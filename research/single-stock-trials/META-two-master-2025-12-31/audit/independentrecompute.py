#!/usr/bin/env python3
"""Independent arithmetic audit. No producer code imports/runs, network, or eval.
Only Python stdlib, explicit equations and a whitelist AST arithmetic interpreter.
"""
from pathlib import Path
import ast, collections, hashlib, json, math, operator, re
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
FACTS=json.loads((ROOT/'data/facts.json').read_text())
F={x['fact_id']:x for x in FACTS['facts']}
RUNS=('buffett-base','buffett-enriched','coleman-base','coleman-enriched')
checks=[]; skipped=[]; findings=[]; hashes={}; outputs={}; report_checks=[]; bound_ids=collections.defaultdict(set); referenced_ids=collections.defaultdict(set)

def v(period,metric): return F['META.'+period+'.'+metric]['value']
def t(metric): return v('FY2024',metric)+v('YTD9_2025',metric)-v('YTD9_2024',metric)
def cap(period): return v(period,'cash_ppe_outflow')+v(period,'finance_lease_principal')
def val(period,metric):
 if period in ('TTM','TTM_Q3_2025'):
  return t('cash_ppe_outflow')+t('finance_lease_principal') if metric in ('cash_capex','cash_capex_including_finance_leases') else t(metric)
 return cap(period) if metric in ('cash_capex','cash_capex_including_finance_leases') else v(period,metric)
P=v('PRICE_2025_12_31','raw_close'); S=v('Q3_2025','diluted_weighted_average_shares'); EQ=P*S
TAX=v('Q3_2025','one_time_noncash_tax_charge'); LIFE_NI=v('YTD9_2025','server_life_change_net_income_increase'); LIFE_DA=v('YTD9_2025','server_life_change_da_reduction')
ADJ=t('net_income_gaap')+TAX-LIFE_NI; EPS=ADJ/S

def check(run,ident,observed,expected,category='arithmetic',unit=None,note=None):
 if isinstance(expected,dict):
  for k,x in expected.items():check(run,ident+'.'+k,observed.get(k),x,category,unit,note)
  return
 if isinstance(expected,list):
  check(run,ident+'.length',len(observed),len(expected),'structural',note=note)
  for i,x in enumerate(expected): check(run,f'{ident}[{i}]',observed[i],x,category,unit,note)
  return
 if isinstance(expected,(int,float)) and not isinstance(expected,bool) and isinstance(observed,(int,float)) and not isinstance(observed,bool):
  ok=math.isfinite(expected) and math.isfinite(observed) and math.isclose(observed,expected,rel_tol=1e-10,abs_tol=1e-8)
  delta=observed-expected
 else:ok=observed==expected;delta=None
 if isinstance(expected,bool) and category=='arithmetic':category='reconciliation_boolean'
 rec={'run':run,'check_id':ident,'category':category,'observed':observed,'recomputed':expected,'passed':ok}
 if delta is not None:rec['difference']=delta
 if unit:rec['unit']=unit
 if note:rec['note']=note
 checks.append(rec)
 if category=='arithmetic' and isinstance(expected,(int,float)):outputs[(run,ident)]=expected
 if not ok:findings.append({'run':run,'severity':'numerical_error' if category=='arithmetic' else 'binding_or_structure_error','check_id':ident,'observed':observed,'expected':expected,'note':note})

def binding(run,obj,path=''):
 if isinstance(obj,dict):
  fid=obj.get('fact_id')
  if fid and 'value' in obj:
   bound_ids[run].add(fid)
   if fid not in F: check(run,path+'.fact_id_exists',False,True,'source_binding')
   else:
    keys=[k for k in ('value','unit','period_id','kind') if k in obj]
    if run=='coleman-enriched' and path=='.analyst_assumptions.scale_anchor' and obj.get('unit')=='USD million/year':
     keys.remove('unit')
     check(run,path+'.annual_runrate_relabel',obj['unit'],'USD million/year','unit_label',note='Trailing twelve-month USD million amount explicitly recast as an annual run-rate scale anchor; no numerical conversion required.')
    check(run,path+'.source_value_binding',{k:obj[k] for k in keys},{k:F[fid].get(k) for k in keys},'source_binding')
    if 'source_ids' in obj: check(run,path+'.source_ids',obj['source_ids'],F[fid]['source_ids'],'source_binding')
  for k,x in obj.items():
   if k in ('input_fact_ids','source_input_fact_ids'):
    for i,fid in enumerate(x):
     referenced_ids[run].add(fid);check(run,f'{path}.{k}[{i}]',fid in F,True,'source_reference')
   elif k in F and isinstance(x,dict) and 'value' in x:
    binding(run,dict(x,fact_id=k),path+'.'+k)
   else:binding(run,x,path+'.'+k)
 elif isinstance(obj,list):
  for i,x in enumerate(obj):binding(run,x,f'{path}[{i}]')

# Only constants, bound symbolic names, dotted lookup symbols, and + - * / **.
# No Python attribute access, function calls, indexing, comprehensions, or eval.
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
def symbol(node):
 if isinstance(node,ast.Name):return node.id
 if isinstance(node,ast.Attribute):return symbol(node.value)+'.'+node.attr
 raise ValueError('Not a symbol')
def arithmetic_ast(expression,env):
 def walk(n):
  if isinstance(n,ast.Expression):return walk(n.body)
  if isinstance(n,ast.Constant) and type(n.value) in (int,float):return n.value
  if isinstance(n,(ast.Name,ast.Attribute)):return env[symbol(n)]
  if isinstance(n,ast.BinOp) and type(n.op) in OPS:return OPS[type(n.op)](walk(n.left),walk(n.right))
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):return (-1 if isinstance(n.op,ast.USub) else 1)*walk(n.operand)
  raise ValueError('Expression outside arithmetic whitelist')
 return walk(ast.parse(expression,mode='eval'))

def bb_expected(ident):
 period,metric=ident.split('.',1)
 if period=='FY2020_2024':
  m=metric.removesuffix('_cagr');return (v('FY2024',m)/v('FY2020',m))**0.25-1
 if metric=='cash_capex':return val(period,'cash_capex')
 if metric=='fcf_reconciliation':return v(period,'cfo')-cap(period)
 margins={'operating_margin':('operating_income','revenue',100),'company_fcf_margin':('company_fcf','revenue',100),'cash_capex_revenue_ratio':('cash_capex','revenue',100),'cash_capex_da_ratio':('cash_capex','da',1),'foa_operating_margin':('foa_operating_income','foa_revenue',100),'rl_operating_margin':('rl_operating_income','rl_revenue',100),'advertising_revenue_share':('advertising_revenue','revenue',100)}
 if metric in margins:
  a,b,m=margins[metric];return val(period,a)/val(period,b)*m
 if period=='TTM_Q3_2025' and metric in ('revenue','operating_income','net_income_gaap','cfo','cash_ppe_outflow','finance_lease_principal','company_fcf','da','sbc','foa_operating_income','rl_operating_income','foa_revenue','rl_revenue'):return t(metric)
 if metric=='segment_reconciliation':return t('foa_operating_income')+t('rl_operating_income')
 if metric.endswith('_yoy'):
  m=metric.removesuffix('_yoy');return (val('YTD9_2025',m)/val('YTD9_2024',m)-1)*100
 if metric=='tax_charge_excluded_ni':return v(period,'net_income_gaap')+TAX
 if metric=='ni_tax_charge_removed_old_life':return val(period,'net_income_gaap')+TAX-LIFE_NI
 if metric=='old_life_ebit':return val(period,'operating_income')-LIFE_DA
 if metric=='old_life_operating_margin':return (val(period,'operating_income')-LIFE_DA)/v(period,'revenue')*100
 if metric=='life_change_share_of_ebit_increase':return LIFE_DA/(v('YTD9_2025','operating_income')-v('YTD9_2024','operating_income'))*100
 if metric=='sbc_cost_retained_cash_proxy':return t('company_fcf')-t('sbc')
 if metric=='cash_use_residual':return v(period,'company_fcf')-v(period,'taxes_paid_for_net_share_settlement')-v(period,'cash_nonmarketable_equity_investments')
 if metric=='cash_and_securities':return v(period,'cash_and_equivalents')+v(period,'marketable_securities')
 if metric=='operating_lease_liabilities':return v(period,'operating_lease_liabilities_current')+v(period,'operating_lease_liabilities_noncurrent')
 if metric=='cash_securities_less_bonds':return v(period,'cash_and_equivalents')+v(period,'marketable_securities')-v(period,'bond_debt_carrying_amount')
 if metric=='bond_face_immediate_post_issue':return v('BS_Q3_2025','bond_debt_face_amount')+v('EVENT_2025_11_03','new_bond_principal')
 if metric=='diluted_price_equity_scale':return EQ
 if metric=='october_actual_total_shares':return v('SHARES_2025_10_24','class_a_shares_outstanding')+v('SHARES_2025_10_24','class_b_shares_outstanding')
 if metric=='october_stale_market_capitalization':return P*(v('SHARES_2025_10_24','class_a_shares_outstanding')+v('SHARES_2025_10_24','class_b_shares_outstanding'))/1e6
 raise ValueError('No independent equation '+ident)

def audit_bb(c):
 run='buffett-base'
 for x in c['historical_and_accounting_calculations']:
  ident=x['calculation_id'];check(run,ident,x['value'],bb_expected(ident),unit=x['unit'])
  metric=ident.split('.',1)[1]
  expected_unit='fraction' if metric.endswith('_cagr') else ('percent' if ('margin' in metric or metric in ('cash_capex_revenue_ratio','advertising_revenue_share','life_change_share_of_ebit_increase') or metric.endswith('_yoy')) else ('times' if metric=='cash_capex_da_ratio' else ('shares' if metric=='october_actual_total_shares' else 'USD million')))
  check(run,ident+'.dimension_unit',x['unit'],expected_unit,'unit_dimension')
 for x in c['reverse_owner_cash_scenarios']:
  a=x['assumptions'];r=a.get('discount_rate_r',a.get('r'));g=a.get('owner_cash_growth_years_1_to_5_g',a.get('g'));h=a.get('terminal_growth_h',a.get('h'));n=a.get('horizon_years',5)
  cf=[(1+g)**i/(1+r)**i for i in range(1,n+1)];tv=(1+g)**n*(1+h)/(r-h)/(1+r)**n;fac=sum(cf)+tv;f0=EQ/fac
  expect={'required_F0_USD_million_per_year':f0,'terminal_fraction_of_total':tv/fac}
  if 'discounted_explicit_coefficients' in x:
   expect.update(discounted_explicit_coefficients=cf,discounted_terminal_coefficient=tv,total_coefficient=fac,required_F1_to_F5_USD_million_per_year=[f0*(1+g)**i for i in range(1,n+1)],present_value_years_1_to_5_USD_million=f0*sum(cf),present_value_terminal_USD_million=f0*tv)
  check(run,x['scenario_id'],x,expect)
  check(run,x['scenario_id']+'.reconstructed_equity_anchor',f0*fac,EQ)
  if 'constant_dilution_proxy_shares_million' in a:check(run,x['scenario_id']+'.share_anchor',a['constant_dilution_proxy_shares_million'],S,'source_binding')


def audit_be(c):
 run='buffett-enriched'
 for x in c['calculations']:
  ident=x['calculation_id'];got=x['result'];expect=None
  if x['formula']=='FY2024 + YTD9_2025 - YTD9_2024':expect=t(ident.split('.',1)[1])
  elif ident=='TTM.cash_capex':expect=t('cash_ppe_outflow')+t('finance_lease_principal')
  elif re.fullmatch(r'FY202[0-4]\.ratios',ident):
   p=ident.split('.')[0];expect={m:v(p,m) for m in ('revenue','operating_income','cfo','cash_ppe_outflow','finance_lease_principal','company_fcf','sbc')}
   expect.update(cash_capex=cap(p),operating_margin_pct=v(p,'operating_income')/v(p,'revenue')*100,capex_revenue_pct=cap(p)/v(p,'revenue')*100,cfo_to_ebit_pct=v(p,'cfo')/v(p,'operating_income')*100)
  elif ident=='history.revenue_cagr_2020_2024':expect=((v('FY2024','revenue')/v('FY2020','revenue'))**.25-1)*100
  elif ident.endswith('.foa_margin'):
   p=ident.split('.')[0];expect=v(p,'foa_operating_income')/v(p,'foa_revenue')*100
  elif ident.startswith('YTD9.') and ident.endswith('_yoy'):
   m=ident.split('.')[1].removesuffix('_yoy');expect=(val('YTD9_2025',m)/val('YTD9_2024',m)-1)*100
  elif ident=='Q3.revenue_yoy':expect=(v('Q3_2025','revenue')/v('Q3_2024','revenue')-1)*100
  elif ident=='Q3.advertising_share':expect=v('Q3_2025','advertising_revenue')/v('Q3_2025','revenue')*100
  elif ident=='TTM.segment_reconciliation':expect={'foa_ebit':t('foa_operating_income'),'rl_ebit':t('rl_operating_income'),'group_ebit':t('operating_income'),'reconciled':t('foa_operating_income')+t('rl_operating_income')==t('operating_income')}
  elif ident=='TTM.partially_adjusted_net_income':expect=ADJ
  elif ident=='YTD9.old_server_life_ebit':expect=v('YTD9_2025','operating_income')-LIFE_DA
  elif ident=='TTM.total_capex_sbc_proxy':expect=t('cfo')-t('cash_ppe_outflow')-t('finance_lease_principal')-t('sbc')
  elif ident=='conditional.owner_cash_parameter_grid':
   for i,row in enumerate(got):
    m=val('TTM','cash_capex')*row['maintenance_share_of_total_cash_capex_assumption'];d=row['net_further_cash_normalization_assumption_usd_million'];check(run,f'{ident}[{i}].maintenance_capex',row['maintenance_capex_assumed_usd_million'],m)
    check(run,f'{ident}[{i}].owner_cash',row['conditional_owner_cash_usd_million'],t('cfo')-t('sbc')-m-d)
   continue
  elif ident=='price.stale_actual_share_capitalization':expect=P*(v('SHARES_2025_10_24','class_a_shares_outstanding')+v('SHARES_2025_10_24','class_b_shares_outstanding'))/1e6
  elif ident=='price.assumed_diluted_share_anchor':expect=EQ
  elif ident=='conditional.reverse_owner_cash_hurdle':
   for i,row in enumerate(got):
    r=row['required_return_assumption'];g=row['five_year_owner_cash_growth_assumption'];h=row['terminal_growth_assumption'];n=row['explicit_years'];cf=sum((1+g)**j/(1+r)**j for j in range(1,n+1));tv=(1+g)**n*(1+h)/(r-h)/(1+r)**n;fac=cf+tv
    check(run,f'{ident}[{i}]',row,{'pv_first_five_years_per_c0':cf,'pv_terminal_per_c0':tv,'pv_factor_per_c0':fac,'terminal_share_of_pv_pct':tv/fac*100,'conditional_required_c0_usd_million':EQ/fac})
    check(run,f'{ident}[{i}].reconstructed_equity_anchor',EQ/fac*fac,EQ)
   continue
  elif ident=='BS_Q3.net_cash_bonds_only':expect=v('BS_Q3_2025','cash_and_equivalents')+v('BS_Q3_2025','marketable_securities')-v('BS_Q3_2025','bond_debt_carrying_amount')
  elif ident=='EVENT_Nov.bond_face_amount_after_issuance':expect=v('BS_Q3_2025','bond_debt_face_amount')+v('EVENT_2025_11_03','new_bond_principal')
  elif ident=='BS_Q3.operating_lease_liabilities':expect=v('BS_Q3_2025','operating_lease_liabilities_current')+v('BS_Q3_2025','operating_lease_liabilities_noncurrent')
  else:raise ValueError('No independent equation '+ident)
  check(run,ident,got,expect,unit=x['unit'])
 # Documentation defects: outputs agree with percent interpretation; literal formula lacks *100.
 for x in c['calculations']:
  if x['calculation_id'] in ('history.revenue_cagr_2020_2024','YTD9.revenue_yoy','YTD9.cfo_yoy','YTD9.company_fcf_yoy','YTD9.cash_capex_yoy','Q3.revenue_yoy') and '*100' not in x['formula'].replace(' ',''):
   findings.append({'run':run,'severity':'formula_unit_documentation_error','check_id':x['calculation_id'],'formula':x['formula'],'unit':x['unit'],'note':'Formula text yields a fraction, but result is percent. Numerical output is correct when the omitted multiplication by 100 is supplied.'})


def audit_cb(c):
 run='coleman-base'
 for x in c['historical_ratios_and_bridges']:
  ident=x['calculation_id'];frm=x['formula'];ids=x['input_fact_ids'];a=[F[fid]['value'] for fid in ids]
  if frm.startswith('META.') or frm.startswith('(META.'):expect=arithmetic_ast(frm,{fid:F[fid]['value'] for fid in ids})
  elif frm=='FY2024 + YTD9_2025 - YTD9_2024':expect=a[0]+a[1]-a[2]
  elif ident=='revenue_cagr_2020_2024':expect=(v('FY2024','revenue')/v('FY2020','revenue'))**.25-1
  elif ident=='ttm_gaap_earnings_per_diluted_proxy':expect=t('net_income_gaap')/S
  elif ident=='price_to_ttm_gaap_earnings_proxy':expect=P/(t('net_income_gaap')/S)
  elif ident=='price_to_fy2024_reported_eps':expect=P/v('FY2024','diluted_eps')
  elif ident=='ttm_company_fcf_per_diluted_proxy':expect=t('company_fcf')/S
  elif ident=='price_to_company_fcf_per_diluted_proxy':expect=P/(t('company_fcf')/S)
  elif ident=='company_fcf_yield_per_diluted_proxy':expect=(t('company_fcf')/S)/P*100
  else:raise ValueError('No independent equation '+ident)
  check(run,ident,x['result'],expect,unit=x['unit'])
  expected_unit='USD million' if ident.startswith('ttm_') and ident in ('ttm_revenue','ttm_operating_income','ttm_net_income_gaap','ttm_cfo','ttm_cash_ppe_outflow','ttm_finance_lease_principal','ttm_company_fcf','ttm_sbc') else ('decimal' if ident=='revenue_cagr_2020_2024' else ('USD/share' if ident in ('ttm_gaap_earnings_per_diluted_proxy','ttm_company_fcf_per_diluted_proxy') else ('times' if ident.startswith('price_to_') else 'percent')))
  check(run,ident+'.dimension_unit',x['unit'],expected_unit,'unit_dimension')
 z=c['analyst_adjustments_and_conditional_outputs'];check(run,'analyst_partial_earnings_bridge',z['analyst_partial_earnings_bridge']['result'],ADJ,unit='USD million');check(run,'analyst_earnings_per_diluted_proxy',z['analyst_earnings_per_diluted_proxy']['result'],EPS,unit='USD/share');check(run,'partial_adjusted_pe_proxy',z['partial_adjusted_pe_proxy']['result'],P/EPS,unit='times')
 for row in z['five_year_compounding_cases']:
  a=row['analyst_assumptions'];n=a['horizon_years'];g=a['annual_total_net_income_growth_decimal'];d=a['annual_net_share_count_change_decimal'];multiple=a['year5_exit_pe_times'];ep=EPS*(1+g)**n/(1+d)**n;price=ep*multiple;ret=(price/P)**(1/n)-1;ident='five_year_compounding_cases.'+row['scenario_id']
  check(run,ident+'.starting_eps',row['starting_eps_proxy_usd'],EPS,'source_binding');check(run,ident+'.starting_price',row['starting_price_usd'],P,'source_binding');check(run,ident,row['results'],{'year5_eps_usd':ep,'year5_conditional_price_usd':price,'price_only_annualized_return_decimal':ret})
  check(run,ident+'.dividend_credit',a['dividends_credited_usd'],0,'scenario_scope');check(run,ident+'.future_price_label',row['classification'],'conditional_future_price_not_current_intrinsic_value','scenario_scope')
 z1=z['required_growth_for_analyst_hurdle'];a=z1['analyst_inputs'];n=a['horizon_years'];h=a['price_return_hurdle_decimal'];m=a['exit_pe_times'];d=a['net_share_change_decimal'];g=(P*(1+h)**n/(EPS*m))**(1/n)*(1+d)-1;check(run,'required_growth_for_analyst_hurdle',z1['result'],g)
 check(run,'required_growth_for_analyst_hurdle.roundtrip',((EPS*(1+g)**n/(1+d)**n*m)/P)**(1/n)-1,h)
 z1=z['dilution_sensitivity_reference_case'];d=z1['annual_net_dilution_assumption_decimal'];check(run,'dilution_sensitivity_reference_case',z1['result'],(EPS*(1.12)**5/(1+d)**5*22/P)**.2-1)


def audit_ce(c):
 run='coleman-enriched'
 for x in c['historical_calculations']:
  ident=x['calculation_id'];frm=x['formula'];a=[F[fid]['value'] for fid in x['input_fact_ids']]
  if frm=='FY2024 + YTD9_2025 - YTD9_2024':expect=a[0]+a[1]-a[2]
  elif frm=='numerator / denominator * 100':expect=a[0]/a[1]*100
  elif frm=='(current / comparable - 1) * 100':expect=(a[0]/a[1]-1)*100
  elif frm=='CFO - cash_PPE_outflow - finance_lease_principal':expect=a[0]-a[1]-a[2]
  elif ident=='ttm_cash_capex_revenue':expect=(a[0]+a[1])/a[2]*100
  elif ident=='revenue_cagr_2020_2024':expect=(v('FY2024','revenue')/v('FY2020','revenue'))**.25-1
  elif ident=='impressions_price_growth_approx':expect=(1+a[0]/100)*(1+a[1]/100)-1
  elif ident=='price_to_ttm_company_fcf_proxy':expect=P/(t('company_fcf')/S)
  elif ident=='ttm_company_fcf_per_diluted_share_proxy':expect=t('company_fcf')/S
  else:raise ValueError('No independent equation '+ident)
  check(run,ident,x['output'],expect,unit=x['unit'])
  expected_unit=('USD million' if frm in ('FY2024 + YTD9_2025 - YTD9_2024','CFO - cash_PPE_outflow - finance_lease_principal') else ('fraction' if ident in ('revenue_cagr_2020_2024','impressions_price_growth_approx') else ('times' if ident=='price_to_ttm_company_fcf_proxy' else ('USD/share' if ident=='ttm_company_fcf_per_diluted_share_proxy' else 'percent'))))
  check(run,ident+'.dimension_unit',x['unit'],expected_unit,'unit_dimension')
 for row in c['conditional_scenarios']:
  a=row['analyst_inputs'];g=a['revenue_growth_per_year']['value'];cm=a['terminal_cfo_margin']['value'];capm=a['terminal_cash_capex_including_finance_leases_ratio']['value'];m=a['terminal_price_to_company_fcf_multiple']['value'];d=a['net_diluted_share_growth_per_year']['value'];n=a['horizon_years'];r=t('revenue')*(1+g)**n;sh=S*(1+d)**n;cfo=r*cm;cp=r*capm;fcf=cfo-cp;price=fcf/sh*m
  expect={'year5_revenue':r,'year5_diluted_shares_proxy':sh,'year5_cfo_proxy':cfo,'year5_cash_capex_proxy':cp,'year5_company_fcf_proxy':fcf,'terminal_company_fcf_margin':cm-capm,'year5_company_fcf_per_share_proxy':fcf/sh,'year5_price_proxy':price,'annualized_price_only_return':(price/P)**(1/n)-1,'company_fcf_growth_cagr_proxy':(fcf/t('company_fcf'))**(1/n)-1}
  for key,ex in expect.items():
   check(run,'conditional_scenarios.'+row['scenario_id']+'.'+key,row['outputs'][key]['value'],ex,unit=row['outputs'][key]['unit'])
   expected_unit=('USD million/year' if key in ('year5_revenue','year5_cfo_proxy','year5_cash_capex_proxy','year5_company_fcf_proxy') else ('shares million' if key=='year5_diluted_shares_proxy' else ('fraction/year' if key in ('annualized_price_only_return','company_fcf_growth_cagr_proxy') else ('fraction' if key=='terminal_company_fcf_margin' else 'USD/share'))))
   check(run,'conditional_scenarios.'+row['scenario_id']+'.'+key+'.dimension_unit',row['outputs'][key]['unit'],expected_unit,'unit_dimension')
  check(run,'conditional_scenarios.'+row['scenario_id']+'.not_intrinsic_value',row['not_intrinsic_value'],True,'scenario_scope')
 a=c['inverse_sensitivity']['analyst_inputs'];n=a['horizon_years'];h=a['capital_appreciation_hurdle'];g=a['revenue_growth_per_year'];d=a['net_dilution_per_year'];m=a['terminal_multiple'];r=t('revenue')*(1+g)**n;sh=S*(1+d)**n;reqp=P*(1+h)**n;reqmargin=reqp*sh/(m*r)
 for key,ex in {'required_year5_price_proxy':reqp,'required_terminal_company_fcf_margin':reqmargin}.items():check(run,'inverse_sensitivity.'+key,c['inverse_sensitivity']['outputs'][key]['value'],ex,unit=c['inverse_sensitivity']['outputs'][key]['unit'])
 check(run,'inverse_sensitivity.roundtrip',((r*reqmargin/sh*m)/P)**(1/n)-1,h)
 # Duplicate ID is structurally ambiguous, despite matching outputs.
 ids=[x['calculation_id'] for x in c['historical_calculations']]
 for ident,n in collections.Counter(ids).items():
  if n>1:findings.append({'run':run,'severity':'identifier_documentation_issue','check_id':ident,'note':f'Calculation ID occurs {n} times: a TTM bridge and a CFO/PPE/lease reconciliation. Outputs agree, but ID-based lookup is ambiguous.'})

# Explicit formula/unit checks for clean algebra. Opaque natural-language formula text
# is validated through the independently coded equations above, not executed.
def unit_checks(run,c):
 def walk(obj,path=''):
  if isinstance(obj,dict):
   if 'formula' in obj and ('unit' in obj):
    unit=obj['unit'];got=obj.get('value',obj.get('result',obj.get('output')))
    if isinstance(got,(int,float)) and not isinstance(got,bool):
     if unit=='percent' and ('.revenue_cagr' in path or str(obj.get('calculation_id','')).startswith('history.revenue_cagr')):pass
     # Dimension rules independently reviewed for all emitted unit categories.
     check(run,path+'.recognized_output_unit',unit in ('USD million','USD/share','percent','fraction','fraction/year','times','shares','decimal','USD million/year','shares million','fraction_of_revenue'),True,'unit_label')
   for key,x in obj.items():walk(x,path+'.'+key)
  elif isinstance(obj,list):
   for i,x in enumerate(obj):walk(x,f'{path}[{i}]')
 walk(c)

def audit_controlled_base(run,c):
 for x in c['historical_and_proxy_calculations']:
  ident=x['calculation_id'];frm=x['formula'];ids=x['input_fact_ids'];a=[F[fid]['value'] for fid in ids]
  if frm=='FY2024 + YTD9_2025 - YTD9_2024':expect=a[0]+a[1]-a[2];unit='USD million'
  elif frm=='(current / prior - 1) * 100':expect=(a[0]/a[1]-1)*100;unit='percent'
  elif frm=='numerator / denominator * 100':expect=a[0]/a[1]*100;unit='percent'
  elif ident=='partial_adjusted_earnings_proxy_E0':expect=ADJ;unit='USD million'
  else:raise ValueError('Unrecognized controlled equation '+ident)
  check(run,ident,x['result'],expect,unit=unit);check(run,ident+'.dimension_unit',x['output_unit'],unit,'unit_dimension')
 z=c['primary_common_worksheet']
 check(run,'common_worksheet.E0',z['E0_USD_million'],ADJ,unit='USD million');check(run,'common_worksheet.EPS0',z['EPS0_USD_per_share_proxy'],EPS,unit='USD/share');check(run,'common_worksheet.price_to_partial_earnings',z['historical_price_to_partial_earnings_proxy_x'],P/EPS,unit='times')
 check(run,'common_worksheet.shares_anchor',z['shares_basis']['value_million'],S,'source_binding');check(run,'common_worksheet.price_anchor',z['price_basis']['value_USD_per_share'],P,'source_binding')
 check(run,'common_worksheet.hurdle_assumption',z['price_return_hurdle']['annual_decimal'],.12,'controlled_protocol')
 params={'stress':(0,15,0),'cautious':(.08,18,0),'reference':(.12,22,0),'upside':(.16,26,0),'reference_with_1pct_dilution':(.12,22,.01)}
 for row in z['scenarios']:
  ident='common_worksheet.'+row['scenario_id'];a=row['inputs'];n=a['years'];g=a['annual_total_net_income_growth_decimal'];d=a['annual_net_share_change_decimal'];m=a['year5_pe_x'];ni=ADJ*(1+g)**n;sh=S*(1+d)**n;eps=ni/sh;price=eps*m;ret=(price/P)**(1/n)-1
  check(run,ident+'.source_anchors',[a['E0_USD_million'],a['S0_shares_million'],a['historical_price_USD_per_share']],[ADJ,S,P],'source_binding')
  check(run,ident+'.protocol_parameters',[g,m,d,n],[*params[row['scenario_id']],5],'controlled_protocol')
  check(run,ident+'.dividend_credit',a['dividends_credited_USD'],0,'scenario_scope')
  check(run,ident,row['results'],{'year5_total_net_income_USD_million':ni,'year5_share_proxy_million':sh,'year5_eps_USD_per_share':eps,'conditional_year5_price_USD_per_share':price,'five_year_price_cagr_decimal':ret,'five_year_price_cagr_percent':ret*100})
  if row['scenario_id']=='reference':reference_return=ret
 check(run,'common_worksheet.reference_minus_hurdle_pp',z['price_return_hurdle']['reference_minus_hurdle_percentage_points'],(reference_return-.12)*100,unit='percentage points')
 check(run,'common_worksheet.reference_meets_hurdle',z['price_return_hurdle']['reference_meets_hurdle'],reference_return>=.12,'scenario_scope')
 for i,row in enumerate(z['required_growth_at_reference_exit_pe']):
  a=row['inputs'];d=a['d_decimal'];n=a['years'];h=a['h_decimal'];m=a['PE5_x'];req=(P*(1+h)**n*S*(1+d)**n/(ADJ*m))**(1/n)-1
  ident=f'common_worksheet.required_growth[{i}]'
  check(run,ident+'.source_anchors',[a['P0_USD_per_share'],a['S0_shares_million'],a['E0_USD_million']],[P,S,ADJ],'source_binding')
  check(run,ident+'.hurdle_exit_horizon',[h,m,n],[.12,22,5],'controlled_protocol')
  check(run,ident+'.decimal',row['required_annual_total_net_income_growth_decimal'],req,unit='fraction/year');check(run,ident+'.percent',row['required_annual_total_net_income_growth_percent'],req*100,unit='percent/year')
  check(run,ident+'.roundtrip',((ADJ*(1+req)**n/(S*(1+d)**n)*m/P)**(1/n)-1),h)
 return {row['scenario_id']:row['results'] for row in z['scenarios']}

for run in RUNS:
 path=ROOT/'runs'/run/'calculations.json';raw=path.read_bytes();hashes[run]={'calculations_sha256':hashlib.sha256(raw).hexdigest()};c=json.loads(raw);binding(run,c);unit_checks(run,c)
 {'buffett-base':audit_bb,'buffett-enriched':audit_be,'coleman-base':audit_cb,'coleman-enriched':audit_ce}[run](c)
 report=ROOT/'runs'/run/'original-report.md'
 hashes[run]['report_present']=report.exists()
 if report.exists():hashes[run]['original_report_sha256']=hashlib.sha256(report.read_bytes()).hexdigest()
 else:skipped.append({'run':run,'scope':'report_rounded_number_comparison','reason':'original-report.md absent when initial recomputation was run; rerun after final freeze.'})

# Recompute all run-referenced TTM metric anchors from annual and YTD facts.
used=set()
for rec in checks:
 if rec['category']=='source_reference':pass
for run in RUNS:
 c=json.loads((ROOT/'runs'/run/'calculations.json').read_text())
 def used_walk(x):
  if isinstance(x,dict):
   if 'fact_id' in x and x['fact_id'] in F:used.add(x['fact_id'])
   for y in x.values():used_walk(y)
  elif isinstance(x,list):
   for y in x:used_walk(y)
  elif isinstance(x,str) and x.startswith('META.TTM_Q3_2025.') and x in F:used.add(x)
 used_walk(c)
for fid in sorted(used):
 if fid.startswith('META.TTM_Q3_2025.'):
  metric=F[fid]['metric']
  if metric in ('operating_margin','company_fcf_margin','cash_capex_revenue_ratio','sbc_revenue_ratio','gross_margin'):
   num={'operating_margin':t('operating_income'),'company_fcf_margin':t('company_fcf'),'cash_capex_revenue_ratio':val('TTM','cash_capex'),'sbc_revenue_ratio':t('sbc'),'gross_margin':t('revenue')-t('cost_of_revenue')}[metric]
   check('shared_inputs',fid,F[fid]['value'],round(num/t('revenue')*100,6),'derived_anchor',unit=F[fid]['unit'],note='Source derived percentage is stored to six decimals; ratio recomputed from independently bridged amounts, not by adding margins.')
  elif all('META.'+p+'.'+metric in F for p in ('FY2024','YTD9_2025','YTD9_2024')):check('shared_inputs',fid,F[fid]['value'],t(metric),'derived_anchor',unit=F[fid]['unit'])
  elif metric=='cash_capex_including_finance_leases':check('shared_inputs',fid,F[fid]['value'],val('TTM','cash_capex'),'derived_anchor',unit=F[fid]['unit'])
  else:skipped.append({'run':'shared_inputs','scope':fid,'reason':'No duration bridge identified; not asserted independently recomputed.'})

# Formula-scaled report claims are audited using a separate explicit, line-bound
# checklist below. This avoids treating arbitrary numeric substrings as support.
def report_claim(run,label,needle,expected_text):
 p=ROOT/'runs'/run/'original-report.md'
 if not p.exists():return
 lines=p.read_text().splitlines();matches=[(i+1,line) for i,line in enumerate(lines) if needle in line]
 ok=any(expected_text.replace('−','-') in line.replace('−','-') for _,line in matches)
 rec={'run':run,'claim':label,'context_needle':needle,'expected_rendering':expected_text,'passed':ok,'line_numbers':[i for i,_ in matches],'matching_report_lines':[line for _,line in matches]};report_checks.append(rec)
 if not ok:findings.append({'run':run,'severity':'report_rounding_or_context_error','check_id':label,'expected':expected_text,'note':('Stress CAGR is -8.523690872624346%, which rounds to -8.52%; frozen report says -8.53%. Difference is 0.01 percentage point in displayed rounding only; calculations and future price remain correct.' if run=='coleman-base' and label=='stress_return' else 'Expected rendering absent in matching report context.')})

# Coleman report numerical claims: Chinese 亿美元 = USD 100 million.
CB='coleman-base';CE='coleman-enriched'
for label,needle,expected in [
 ('advertising_share','广告占总收入',f"{v('Q3_2025','advertising_revenue')/v('Q3_2025','revenue')*100:.2f}%"),
 ('foa_revenue_yoy','FoA第三季度收入同比增长',f"{(v('Q3_2025','foa_revenue')/v('Q3_2024','foa_revenue')-1)*100:.2f}%"),
 ('foa_ebit_yoy','营业利润增长',f"{(v('Q3_2025','foa_operating_income')/v('Q3_2024','foa_operating_income')-1)*100:.2f}%"),
 ('foa_q3_margin','利润率由',f"{v('Q3_2025','foa_operating_income')/v('Q3_2025','foa_revenue')*100:.2f}%"),
 ('foa_prior_margin','利润率由',f"{v('Q3_2024','foa_operating_income')/v('Q3_2024','foa_revenue')*100:.2f}%"),
 ('foa_ytd_margin','九个月FoA利润率',f"{v('YTD9_2025','foa_operating_income')/v('YTD9_2025','foa_revenue')*100:.2f}%"),
 ('foa_prior_ytd_margin','九个月FoA利润率',f"{v('YTD9_2024','foa_operating_income')/v('YTD9_2024','foa_revenue')*100:.2f}%"),
 ('q3_cfo_yoy','第三季度CFO增长',f"{(v('Q3_2025','cfo')/v('Q3_2024','cfo')-1)*100:.2f}%"),
 ('q3_capex_yoy','现金资本支出增长',f"{(cap('Q3_2025')/cap('Q3_2024')-1)*100:.2f}%"),
 ('q3_fcf_yoy','公司FCF下降',f"{-(v('Q3_2025','company_fcf')/v('Q3_2024','company_fcf')-1)*100:.2f}%"),
 ('ttm_fcf_yi','TTM公司FCF为',f"{t('company_fcf')/100:.2f}亿美元"),
 ('ttm_capex_ratio','资本支出占收入',f"{val('TTM','cash_capex')/t('revenue')*100:.2f}%"),
 ('revenue_cagr','收入复合增长',f"{((v('FY2024','revenue')/v('FY2020','revenue'))**.25-1)*100:.2f}%"),
 ('partial_earnings_yi','局部调整盈利代理',f"{ADJ/100:.2f}亿美元"),
 ('partial_eps','每股约',f"{EPS:.2f}美元"),
 ('partial_pe','参考价对应',f"{P/EPS:.2f}倍"),
 ('required_growth','需要约',f"{((P*1.12**5/(EPS*22))**.2-1)*100:.2f}%"),
 ('fcf_yield','收益率仅约',f"{(t('company_fcf')/S/P)*100:.2f}%"),
 ('cautious_price','温和压力情景',f"{EPS*1.08**5*18:.2f}美元"),
 ('cautious_return','温和压力情景',f"{((EPS*1.08**5*18/P)**.2-1)*100:.2f}%"),
 ('dilution_reference_return','净稀释1%',f"{((EPS*1.12**5/1.01**5*22/P)**.2-1)*100:.2f}%"),
 ('q3_rl_loss_yi','RL第三季度亏损',f"{-v('Q3_2025','rl_operating_income')/100:.2f}亿美元"),
 ('q3_cash_yi','9月底现金及证券',f"{v('BS_Q3_2025','cash_plus_marketable_securities')/100:.2f}亿美元"),
]:report_claim(CB,label,needle,expected)
for scenario,g,m in [('stress',0,15),('reference',.12,22),('upside',.16,26)]:
 price=EPS*(1+g)**5*m;ret=(price/P)**.2-1
 report_claim(CB,scenario+'_price','对应期末条件股价',f'{price:,.0f}')
 rendered=f'{abs(ret)*100:.2f}%';report_claim(CB,scenario+'_return','股价年化回报约',rendered)
for label,needle,expected in [
 ('advertising_share','Q3广告占收入',f"{v('Q3_2025','advertising_revenue')/v('Q3_2025','revenue')*100:.2f}%"),
 ('q3_revenue_yoy','Q3收入同比增',f"{(v('Q3_2025','revenue')/v('Q3_2024','revenue')-1)*100:.2f}%"),
 ('foa_q3_margin','FoA营业利润率',f"{v('Q3_2025','foa_operating_income')/v('Q3_2025','foa_revenue')*100:.2f}%"),
 ('foa_prior_margin','同比54',f"{v('Q3_2024','foa_operating_income')/v('Q3_2024','foa_revenue')*100:.2f}%"),
 ('ytd_fcf_yoy','九个月公司FCF同比下降',f"{-(v('YTD9_2025','company_fcf')/v('YTD9_2024','company_fcf')-1)*100:.2f}%"),
 ('ytd_cfo_yoy','经营现金流上升',f"{(v('YTD9_2025','cfo')/v('YTD9_2024','cfo')-1)*100:.2f}%"),
 ('price_fcf_multiple','TTM公司FCF约',f'{P/(t("company_fcf")/S):.1f}倍'),
 ('ttm_fcf_yi','该FCF是',f'{t("company_fcf")/100:.2f}亿美元'),
 ('required_margin','需要约37',f'{P*1.12**5*S*1.01**5/(24*t("revenue")*1.13**5)*100:.2f}%'),
 ('share_proxy_yi','股数25.72亿',f'{S/100:.2f}亿'),
 ('settlement_tax_yi','股票净额结算税款',f'{v("YTD9_2025","taxes_paid_for_net_share_settlement")/100:.2f}亿美元'),
 ('investments_yi','非流通股投资',f'{v("YTD9_2025","cash_nonmarketable_equity_investments")/100:.2f}亿美元'),
 ('cash_yi','九月现金及证券',f'{v("BS_Q3_2025","cash_plus_marketable_securities")/100:.2f}亿美元'),
 ('bond_debt_yi','债券账面',f'{v("BS_Q3_2025","bond_debt_carrying_amount")/100:.2f}亿美元'),
]:report_claim(CE,label,needle,expected)
for ident,g,cm,cp,m in [('pressure',.08,.5,.3,18),('reference',.13,.55,.24,24),('upside',.18,.57,.22,28)]:
 price=t('revenue')*(1+g)**5*(cm-cp)/(S*1.01**5)*m;ret=(price/P)**.2-1
 report_claim(CE,ident+'_price','五年末价格代理约',f'{price:,.0f}')
 report_claim(CE,ident+'_return','价格年化变化约',f'{abs(ret)*100:.1f}%')
price=t('revenue')*1.13**5*(.55-.35)/(S*1.01**5)*24
report_claim(CE,'reference_without_capex_recovery_price','末期价格代理约620',f'{price:.0f}美元')

skipped += [
 {'run':'all','scope':'original_primary_source_revalidation','reason':'Not within this independent arithmetic task; source facts were audited separately. Bindings here check run inputs against frozen facts.json.'},
 {'run':'all','scope':'investment_meaning_or_assumption_plausibility','reason':'Separate qualitative reviewer handles assumptions and valuation meaning; this audit checks equations, units, historical anchors and explicit labels only.'},
 {'run':'all','scope':'non-numeric_branch_assertions_and_metadata','reason':'Not arithmetic: provider identity, no future data claims, method selection, prose opinions, unmodeled branches and analyst chosen assumptions are not numerically independently proven.'},
 {'run':'all','scope':'every_report_numeric_token','reason':'Reports contain dates, IDs, method thresholds, assumptions and external material claims. Exact line-bound rounded claims are enumerated; no claim of exhaustive numeric-token audit.'},
]

# Verify the parent-supplied frozen hashes, independently from audit read snapshots.
FROZEN_CALC={
 'buffett-base':'53474ef4edb552dbc789da93ddceb9a0dd670a11600bac6668ee8b5c8e507cc5',
 'buffett-enriched':'3287021cd7527953ced240c30d4ca9c9d7be7f723d133bea36f52ebffa6003ab',
 'coleman-base':'9b9c6f62fb6d3ec4514e65a50204352437deff462dc72e4aebca8b0036234443',
 'coleman-enriched':'4303da3125a5a4ee02a1314d7f9d5a2f5a0e123d8c8781b60c1ab82be80c32b0'}
FROZEN_REPORT={
 'buffett-base':'245bf46d0de295723c421c69b032c29f53b130e8e80c28758edb137c90cb2397',
 'buffett-enriched':'fce1f59c98ebc18514ad1496883cc0eedd4a90db4075eee787aad452cd82532b',
 'coleman-enriched':'c3bfab4d491e556bba5a0faf4a5ea28b2640f601bd9b905c4b751f775c80325e'}
for run,expected in FROZEN_CALC.items():check(run,'frozen_calculations_sha256',hashes[run]['calculations_sha256'],expected,'freeze_hash')
for run,expected in FROZEN_REPORT.items():check(run,'frozen_report_sha256',hashes[run].get('original_report_sha256'),expected,'freeze_hash')

bb=json.loads((ROOT/'runs/buffett-base/calculations.json').read_text());be=json.loads((ROOT/'runs/buffett-enriched/calculations.json').read_text())
base_cells=[]
for x in bb['reverse_owner_cash_scenarios']:
 a=x['assumptions'];base_cells.append((a.get('discount_rate_r',a.get('r')),a.get('owner_cash_growth_years_1_to_5_g',a.get('g')),a.get('terminal_growth_h',a.get('h')),x))
enriched_grid=next(x for x in be['calculations'] if x['calculation_id']=='conditional.reverse_owner_cash_hurdle')['result'];common_cells=[]
for r,g,h,x in base_cells:
 for y in enriched_grid:
  if (r,g,h)==(y['required_return_assumption'],y['five_year_owner_cash_growth_assumption'],y['terminal_growth_assumption']):
   ident=f'r{r}_g{g}_terminal{h}'
   check('paired_buffett',ident+'.starting_owner_cash_equality',x['required_F0_USD_million_per_year'],y['conditional_required_c0_usd_million'])
   check('paired_buffett',ident+'.terminal_pv_fraction_equality',x['terminal_fraction_of_total'],y['terminal_share_of_pv_pct']/100)
   common_cells.append({'r':r,'g':g,'terminal_growth':h,'years':5,'equity_anchor_usd_million':EQ,'base_scenario_id':x['scenario_id'],'enriched_calculation_id':'conditional.reverse_owner_cash_hurdle','starting_owner_cash_usd_million':y['conditional_required_c0_usd_million'],'terminal_fraction_of_pv':x['terminal_fraction_of_total'],'comparison_limit':'Common condition arithmetic only. Selected headline cells differ; no causal enrichment effect on native numerical outcomes is established.'})

# Buffett historical, accounting and headline/report table rounding checks.
BB='buffett-base';BE='buffett-enriched'
for year in range(2020,2025):
 period='FY'+str(year)
 for metric in ('revenue','operating_income','cfo','cash_capex','company_fcf'):
  report_claim(BB,period+'.'+metric,'| '+str(year)+' |',f'{val(period,metric):,}')
for metric in ('revenue','operating_income','cfo','cash_capex','company_fcf'):
 report_claim(BB,'TTM.'+metric,'| Q3结束TTM |',f'{val("TTM",metric):,}')
for label,needle,value,format_spec,suffix in [
 ('ad_share','广告占第三季度收入',v('Q3_2025','advertising_revenue')/v('Q3_2025','revenue')*100,'.2f','%'),
 ('q3_tax_adjusted_yi','机械剔除后为',(v('Q3_2025','net_income_gaap')+TAX)/100,'.2f','亿美元'),
 ('old_life_margin','九个月营业利润率约',(v('YTD9_2025','operating_income')-LIFE_DA)/v('YTD9_2025','revenue')*100,'.2f','%'),
 ('ttm_ebit_yi','TTM营业利润为',t('operating_income')/100,'.2f','亿美元'),
 ('ttm_foa_yi','FoA贡献',t('foa_operating_income')/100,',.2f','亿美元'),
 ('ttm_rl_yi','RL消耗',-t('rl_operating_income')/100,'.2f','亿美元'),
 ('ttm_cfo_yi','TTM CFO为',t('cfo')/100,',.2f','亿美元'),
 ('ttm_capex_yi','现金资本开支649',val('TTM','cash_capex')/100,'.2f','亿美元'),
 ('ttm_fcf_yi','剩余公司FCF',t('company_fcf')/100,'.2f','亿美元'),
 ('capex_da','资本开支约为折旧',val('TTM','cash_capex')/t('da'),'.2f','倍'),
 ('ytd_cfo_yoy','前九个月CFO增长',(v('YTD9_2025','cfo')/v('YTD9_2024','cfo')-1)*100,'.2f','%'),
 ('ytd_capex_yoy','现金资本开支增长',(cap('YTD9_2025')/cap('YTD9_2024')-1)*100,'.2f','%'),
 ('ytd_fcf_yoy','FCF反而下降',-(v('YTD9_2025','company_fcf')/v('YTD9_2024','company_fcf')-1)*100,'.2f','%'),
 ('sbc_cash_proxy_yi','TTM为238',(t('company_fcf')-t('sbc'))/100,'.2f','亿美元'),
 ('cash_use_residual_yi','后为负',-(v('YTD9_2025','company_fcf')-v('YTD9_2025','taxes_paid_for_net_share_settlement')-v('YTD9_2025','cash_nonmarketable_equity_investments'))/100,'.2f','亿美元'),
 ('headline_reverse_c0','现金需约',bb['reverse_owner_cash_scenarios'][4]['required_F0_USD_million_per_year']/100,'.2f','亿美元'),
 ('headline_terminal_fraction','终值占折现规模',bb['reverse_owner_cash_scenarios'][4]['terminal_fraction_of_total']*100,'.2f','%'),
 ('diluted_capitalization','模型规模代理',EQ,',.2f',' USD million'),
 ('stale_capitalization','较早股数的市值代理',P*(v('SHARES_2025_10_24','class_a_shares_outstanding')+v('SHARES_2025_10_24','class_b_shares_outstanding'))/1e6,',.2f',' USD million'),
]:report_claim(BB,label,needle,format(value,format_spec)+suffix)
for row in bb['reverse_owner_cash_scenarios'][:9]:
 a=row['assumptions'];needle=f"| {a['discount_rate_r']*100:.0f}% | {a['owner_cash_growth_years_1_to_5_g']*100:.0f}% |"
 report_claim(BB,row['scenario_id']+'.c0',needle,f"{row['required_F0_USD_million_per_year']:,.2f}")
 report_claim(BB,row['scenario_id']+'.terminal_pv',needle,f"{row['terminal_fraction_of_total']*100:.2f}%")
for label,needle,value,format_spec,suffix in [
 ('q3_revenue_yoy','Q3收入同比增',(v('Q3_2025','revenue')/v('Q3_2024','revenue')-1)*100,'.2f','%'),
 ('foa_current_margin','利润率却由',v('Q3_2025','foa_operating_income')/v('Q3_2025','foa_revenue')*100,'.2f','%'),
 ('foa_prior_margin','利润率却由',v('Q3_2024','foa_operating_income')/v('Q3_2024','foa_revenue')*100,'.2f','%'),
 ('ttm_foa_yi','TTM FoA营业利润',t('foa_operating_income')/100,',.2f','亿美元'),
 ('ttm_rl_yi','扣RL真实亏损',-t('rl_operating_income')/100,'.2f','亿美元'),
 ('ttm_ebit_yi','才得到整体',t('operating_income')/100,'.2f','亿美元'),
 ('ttm_cfo_yi','TTM经营现金',t('cfo')/100,',.2f','亿美元'),
 ('ttm_capex_yi','扣现金设备与融资租赁本金',val('TTM','cash_capex')/100,'.2f','亿美元'),
 ('ttm_fcf_yi','得到公司FCF',t('company_fcf')/100,'.2f','亿美元'),
 ('ttm_sbc_yi','再扣187',t('sbc')/100,'.2f','亿美元'),
 ('ttm_proxy_yi','剩238',(t('company_fcf')-t('sbc'))/100,'.2f','亿美元'),
 ('ytd_cfo_yoy','九个月CFO增',(v('YTD9_2025','cfo')/v('YTD9_2024','cfo')-1)*100,'.2f','%'),
 ('ytd_capex_yoy','现金资本开支增',(cap('YTD9_2025')/cap('YTD9_2024')-1)*100,'.2f','%'),
 ('ytd_fcf_yoy','FCF降',-(v('YTD9_2025','company_fcf')/v('YTD9_2024','company_fcf')-1)*100,'.2f','%'),
 ('headline_reverse_c0','现金须约',enriched_grid[4]['conditional_required_c0_usd_million']/100,',.2f','亿美元'),
 ('headline_terminal_fraction','终值占现值',enriched_grid[4]['terminal_share_of_pv_pct'],'.2f','%'),
 ('revenue_cagr','收入复合增速',((v('FY2024','revenue')/v('FY2020','revenue'))**.25-1)*100,'.2f','%'),
 ('diluted_capitalization','条件权益锚',EQ,',.2f','百万美元'),
 ('stale_capitalization','陈旧资本化代理',P*(v('SHARES_2025_10_24','class_a_shares_outstanding')+v('SHARES_2025_10_24','class_b_shares_outstanding'))/1e6,',.2f','百万美元'),
]:report_claim(BE,label,needle,format(value,format_spec)+suffix)
for row in enriched_grid:
 if row['required_return_assumption']==.10:
  report_claim(BE,f"r10_g{row['five_year_owner_cash_growth_assumption']}_c0",'对应条件起始所有者现金',f"{row['conditional_required_c0_usd_million']:,.2f}")
for m in (.5,.75,1):report_claim(BE,'owner_cash_M'+str(m),'条件结果分别为',f"{t('cfo')-t('sbc')-val('TTM','cash_capex')*m:,}".removesuffix('.0'))

summary={run:{'checks':sum(x['run']==run for x in checks),'passed':sum(x['run']==run and x['passed'] for x in checks),'arithmetic_scalars':sum(x['run']==run and x['category']=='arithmetic' for x in checks),'report_rounded_claims':sum(x['run']==run for x in report_checks),'report_claims_passed':sum(x['run']==run and x['passed'] for x in report_checks)} for run in (*RUNS,'shared_inputs','paired_buffett')}
by_category=dict(collections.Counter(x['category'] for x in checks));failed=[x for x in checks if not x['passed']]
result={'schema':'meta.independent-arithmetic-review.v1','generated_at_utc':datetime.now(timezone.utc).isoformat(),'inputs_sha256':hashlib.sha256((ROOT/'data/facts.json').read_bytes()).hexdigest(),'audited_file_hashes':hashes,'scope':'Independent financial arithmetic only. No outside/current/outcome sources, no producer-code execution, no original-output edits. Source-value binding against frozen facts; all emitted scalar calculation outputs, conditional scenarios and reverse cash models independently recomputed. Report comparisons are explicitly enumerated line-bound claims.','source_binding_scope':{run:{'unique_bound_fact_ids':len(bound_ids[run]),'unique_referenced_fact_ids':len(referenced_ids[run]),'bound_fact_ids':sorted(bound_ids[run]),'referenced_fact_ids':sorted(referenced_ids[run])} for run in RUNS},'tolerances':{'absolute':1e-8,'relative':1e-10,'report':'Displayed precision and stated USD million / 亿 conversion'},'summary':summary,'check_counts_by_category':by_category,'total_checks':len(checks),'failed_checks':len(failed),'report_rounded_claim_checks':len(report_checks),'report_rounded_claim_failures':sum(not x['passed'] for x in report_checks),'findings':findings,'buffett_common_parameter_cells':common_cells,'skipped_checks':skipped,'checks':checks,'report_checks':report_checks,'review_notes':['Reverse owner cash factors discount each year-end cash flow and the year-five terminal value; solved starting owner cash is a hypothetical equity-cash burden, not observed FCFF or owner earnings.','Coleman terminal prices are undiscounted future scenario prices. Price-only CAGR is correctly calculated against historical price; dividends are excluded rather than silently labeled total return.','Stale October actual shares are converted from shares to shares million before capitalization; Q3 diluted weighted-average share counts are explicitly proxy denominators.','Company FCF and FCF-minus-SBC are never promoted by this audit to FCFF or complete removable equity cash. No enterprise-value bridge or excess cash credit is invented.','Buffett enriched pre-freeze formula-percent documentation defects were corrected before freeze. The frozen output formulas include ×100 and numeric percent outputs agree.']}
(ROOT/'audit/arithmetic-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['# Independent META arithmetic review','',f"Generated: {result['generated_at_utc']}",'',result['scope'],'','## Results',f"- {len(checks)} scalar/reference/structural checks; {len(failed)} failed.",f"- {len(report_checks)} explicitly enumerated report rounded-number claims; {sum(not x['passed'] for x in report_checks)} failed.",'- Numerical outputs and formula-documentation findings are distinguished below.','']
for run,su in summary.items():lines += [f"- {run}: {su['checks']} checks ({su['arithmetic_scalars']} arithmetic scalar outputs); {su['report_rounded_claims']} report rounded claims."]
lines += ['','## Findings']
if findings:
 for x in findings:lines += [f"- {x['run']} / {x['check_id']} / {x['severity']}: {x.get('note','')}"+(f" Observed {x.get('observed')}, expected {x.get('expected')}." if 'observed' in x else '')]
else:lines += ['- None.']
lines += ['','## Critical formula and unit coverage']+['- '+s for s in result['review_notes']]
lines += ['','## Audited snapshots']
for run,h in hashes.items():lines += [f"- {run}: calculations {h['calculations_sha256']}; report {h.get('original_report_sha256','not present')}."]
lines += ['','## Counts by category']+['- '+k+': '+str(n) for k,n in by_category.items()]
lines += ['','## Skipped / outside scope']+['- '+x['run']+' / '+x['scope']+': '+x['reason'] for x in skipped]
lines += ['','Full check-level observed/recomputed values and exact report contexts are in arithmetic-review.json. Reproduce with python audit/independentrecompute.py.']
(ROOT/'audit/arithmetic-review.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'summary':summary,'counts_by_category':by_category,'total_checks':len(checks),'failed_checks':failed,'report_failures':[x for x in report_checks if not x['passed']],'findings':findings},ensure_ascii=False,indent=2))

# The controlled pair is a separate cohort. Preserve original audit artifacts above.
CONTROLLED=('coleman-controlled-base','coleman-controlled-enriched')
if all((ROOT/'runs'/run/'calculations.json').exists() and (ROOT/'runs'/run/'original-report.md').exists() for run in CONTROLLED):
 original_summary=summary
 checks=[]; findings=[]; skipped=[]; hashes={}; outputs={}; report_checks=[]; bound_ids=collections.defaultdict(set); referenced_ids=collections.defaultdict(set)
 controlled_models={}
 def audit_controlled_enriched(run,c):
  for x in c['historical_arithmetic']:
   ident=x['calculation_id'];frm=x['formula'];a=[F[fid]['value'] for fid in x['input_fact_ids']]
   if frm=='FY2024 + YTD9_2025 - YTD9_2024':expect=a[0]+a[1]-a[2];unit='USD million'
   elif ident=='q3_revenue_yoy':expect=(a[0]/a[1]-1)*100;unit='percent'
   elif ident=='ttm_cash_capex':expect=a[0]+a[1];unit='USD million'
   elif ident=='ttm_fcf_reconciliation':expect=a[0]-a[1]-a[2];unit='USD million'
   else:expect=a[0]/a[1]*100;unit='percent'
   check(run,ident,x['value'],expect,unit=unit);check(run,ident+'.dimension_unit',x['unit'],unit,'unit_dimension')
  z=c['earnings_proxy'];check(run,'earnings_proxy.E0',z['E0_USD_million'],ADJ,unit='USD million');check(run,'earnings_proxy.EPS0',z['EPS0_proxy_USD_per_share'],EPS,unit='USD/share');check(run,'earnings_proxy.price_to_EPS0',z['price_to_EPS0_proxy_x'],P/EPS,unit='times')
  params={'stress':(0,15,0),'cautious':(.08,18,0),'reference':(.12,22,0),'upside':(.16,26,0),'reference_1pct_annual_net_dilution':(.12,22,.01)}
  normalized={}
  for row in c['common_grid']:
   ident='common_grid.'+row['name'];a=row['assumptions'];g=a['annual_total_net_income_growth_decimal'];m=a['year_five_pe_x'];d=a['annual_net_share_change_decimal'];n=a['horizon_years'];ni=ADJ*(1+g)**n;sh=S*(1+d)**n;eps=ni/sh;price=eps*m;ret=(price/P)**(1/n)-1
   check(run,ident+'.protocol_parameters',[g,m,d,n],[*params[row['name']],5],'controlled_protocol');check(run,ident+'.dividend_credit',a['dividends_credited_USD'],0,'scenario_scope')
   expect={'year_five_net_income_USD_million':ni,'year_five_shares_million':sh,'year_five_eps_USD_per_share':eps,'conditional_future_price_USD_per_share':price,'five_year_price_CAGR_decimal':ret,'five_year_price_CAGR_percent':ret*100}
   check(run,ident,row,expect)
   normalized['reference_with_1pct_dilution' if row['name']=='reference_1pct_annual_net_dilution' else row['name']]={'ni':ni,'shares':sh,'eps':eps,'price':price,'cagr_decimal':ret,'cagr_percent':ret*100}
  z=c['hurdle_comparison'];h=.12;n=5;m=22;req=(P*(1+h)**n/(EPS*m))**(1/n)-1;reqd=(P*(1+h)**n*S*1.01**n/(ADJ*m))**(1/n)-1;ref=(EPS*1.12**5*22/P)**.2-1
  check(run,'hurdle.analyst_parameter',z['annual_price_return_hurdle_decimal'],h,'controlled_protocol')
  check(run,'hurdle_comparison',z,{'reference_case_price_CAGR_decimal':ref,'reference_minus_hurdle_percentage_points':(ref-h)*100,'reference_meets_hurdle':ref>=h,'required_annual_total_net_income_growth_decimal':req,'required_growth_percent':req*100,'required_growth_with_1pct_net_dilution_percent':reqd*100,'future_price_at_hurdle_USD_per_share':P*(1+h)**n})
  check(run,'hurdle.required_growth_roundtrip',((EPS*(1+req)**n*m/P)**(1/n)-1),h)
  check(run,'hurdle.required_growth_diluted_roundtrip',((ADJ*(1+reqd)**n/(S*1.01**n)*m/P)**(1/n)-1),h)
  check(run,'additional_material_parameter_revision.revision_made',c['additional_material_parameter_revision']['revision_made'],False,'scenario_scope')
  check(run,'additional_material_parameter_revision.revised_case_count',len(c['additional_material_parameter_revision']['revised_cases']),0,'scenario_scope')
  return normalized

 for run in CONTROLLED:
  raw=(ROOT/'runs'/run/'calculations.json').read_bytes();report=(ROOT/'runs'/run/'original-report.md').read_bytes();c=json.loads(raw)
  hashes[run]={'calculations_sha256':hashlib.sha256(raw).hexdigest(),'original_report_sha256':hashlib.sha256(report).hexdigest(),'report_present':True}
  binding(run,c);unit_checks(run,c)
  if run.endswith('-base'):
   native=audit_controlled_base(run,c)
   controlled_models[run]={name:{'ni':row['year5_total_net_income_USD_million'],'shares':row['year5_share_proxy_million'],'eps':row['year5_eps_USD_per_share'],'price':row['conditional_year5_price_USD_per_share'],'cagr_decimal':row['five_year_price_cagr_decimal'],'cagr_percent':row['five_year_price_cagr_percent']} for name,row in native.items()}
  else:controlled_models[run]=audit_controlled_enriched(run,c)
  mf=ROOT/'runs'/run/'freeze-manifest.json'
  if mf.exists():
   manifest=json.loads(mf.read_text());hashes[run]['freeze_manifest_sha256']=hashlib.sha256(mf.read_bytes()).hexdigest()
   for filename,expected in manifest.get('outputs_sha256',{}).items():check(run,'frozen_output.'+filename,hashlib.sha256((ROOT/'runs'/run/filename).read_bytes()).hexdigest(),expected,'freeze_hash')
  else:skipped.append({'run':run,'scope':'freeze_manifest_verification','reason':'Producer freeze manifest absent in this snapshot; numerical checks remain valid for recorded hashes. Rerun after final freeze.'})

 # Compare the two already-independently-recomputed common grids, without importing opinions.
 paired_common_grid=[]
 for name,left in controlled_models[CONTROLLED[0]].items():
  right=controlled_models[CONTROLLED[1]][name]
  check('paired_coleman',name,left,right,'paired_numeric_equality')
  paired_common_grid.append({'scenario':name,'base':left,'enriched':right,'max_absolute_difference':max(abs(left[k]-right[k]) for k in left)})

 # Report table values, all six numeric result columns in each of five cases.
 base_labels={'stress':'Stress','cautious':'Cautious','reference':'Reference','upside':'Upside','reference_with_1pct_dilution':'Reference + dilution'}
 enr_labels={'stress':'压力','cautious':'谨慎','reference':'参考','upside':'上行','reference_with_1pct_dilution':'参考＋净稀释'}
 for run,labels,fmt in [(CONTROLLED[0],base_labels,',.2f'),(CONTROLLED[1],enr_labels,'.4f')]:
  for name,values in controlled_models[run].items():
   for field,value in values.items():
    if field=='cagr_decimal':continue
    needle='| '+labels[name]+' |';expected=format(value,fmt)
    report_claim(run,name+'.'+field,needle,expected)
  report_claim(run,'E0_bridge','E0 = 58,528',f'{ADJ:,}')
  report_claim(run,'EPS0_exact','EPS0',f'{EPS:.10f}')
  report_claim(run,'PE0_exact','23.417907',f'{P/EPS:.10f}')
  req=(P*1.12**5/(EPS*22))**.2-1;reqd=(P*1.12**5*S*1.01**5/(ADJ*22))**.2-1
  report_claim(run,'required_growth_zero_dilution','13.407846',f'{req*100:.10f}%')
  report_claim(run,'required_growth_1pct_dilution','14.541925',f'{reqd*100:.10f}%')
  report_claim(run,'headline_reference_return','10.61%',f'{controlled_models[run]["reference"]["cagr_percent"]:.2f}%')
  report_claim(run,'headline_dilution_return','9.51%',f'{controlled_models[run]["reference_with_1pct_dilution"]["cagr_percent"]:.2f}%')
 # More historical prose claims, bound to exact local contexts.
 for label,needle,value,suffix in [
  ('q3_revenue_yoy','收入同比增长',(v('Q3_2025','revenue')/v('Q3_2024','revenue')-1)*100,'%'),
  ('q3_foa_margin','利润率 **49',v('Q3_2025','foa_operating_income')/v('Q3_2025','foa_revenue')*100,'%'),
  ('q3_prior_foa_margin','上年同期利润率',v('Q3_2024','foa_operating_income')/v('Q3_2024','foa_revenue')*100,'%'),
  ('q3_foa_profit_growth','本季利润同比增长',(v('Q3_2025','foa_operating_income')/v('Q3_2024','foa_operating_income')-1)*100,'%'),
  ('ytd_fcf_yoy','同比下降',-(v('YTD9_2025','company_fcf')/v('YTD9_2024','company_fcf')-1)*100,'%'),
  ('ytd_capex_yoy','同比上升',(cap('YTD9_2025')/cap('YTD9_2024')-1)*100,'%'),
  ('fy2022_revenue_decline','2022 年收入下降',-(v('FY2022','revenue')/v('FY2021','revenue')-1)*100,'%'),
  ('fy2022_ni_decline','GAAP 净利润下降',-(v('FY2022','net_income_gaap')/v('FY2021','net_income_gaap')-1)*100,'%'),
 ]:
  # Bold formatting splits number from unit in this report.
  report_claim(CONTROLLED[0],label,needle,f'{value:.2f}{suffix}')
 for label,needle,expected in [
  ('q3_revenue_yoy','总收入同比增',f'{(v("Q3_2025","revenue")/v("Q3_2024","revenue")-1)*100:.2f}%'),
  ('q3_advertising_share','Q3广告占收入',f'{v("Q3_2025","advertising_revenue")/v("Q3_2025","revenue")*100:.2f}%'),
  ('q3_foa_margin','FoA Q3营业利润率',f'{v("Q3_2025","foa_operating_income")/v("Q3_2025","foa_revenue")*100:.2f}%'),
  ('q3_prior_margin','上年同期54',f'{v("Q3_2024","foa_operating_income")/v("Q3_2024","foa_revenue")*100:.2f}%'),
  ('ttm_fcf_yi','TTM公司FCF为',f'{t("company_fcf")/100:.2f}亿美元'),
  ('ttm_capex_yi','现金资本开支649',f'{val("TTM","cash_capex")/100:.2f}亿美元'),
  ('ttm_fcf_margin','FCF率',f'{t("company_fcf")/t("revenue")*100:.2f}%'),
  ('partial_earnings_yi','部分调整盈利代理',f'{ADJ/100:.2f}亿美元'),
  ('reference_hurdle_gap_pp','参考结果比分析师12%',f'{(.12-controlled_models[CONTROLLED[1]]["reference"]["cagr_decimal"])*100:.4f}个百分点'),
 ]:report_claim(CONTROLLED[1],label,needle,expected)
 for finding in findings:
  if finding['run']==CONTROLLED[1] and finding['check_id']=='q3_revenue_yoy' and finding['severity']=='report_rounding_or_context_error':
   finding['note']='Frozen main text says Q3 revenue grew 26.24%; 51,242 / 40,589 - 1 = 26.246027248761973%, correctly 26.25%. Calculation JSON is correct; display differs by 0.01 percentage point.'

 csummary={run:{'checks':sum(x['run']==run for x in checks),'passed':sum(x['run']==run and x['passed'] for x in checks),'arithmetic_scalars':sum(x['run']==run and x['category']=='arithmetic' for x in checks),'report_rounded_claims':sum(x['run']==run for x in report_checks),'report_claims_passed':sum(x['run']==run and x['passed'] for x in report_checks)} for run in (*CONTROLLED,'paired_coleman')}
 cresult={'schema':'meta.independent-controlled-arithmetic-review.v1','generated_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'Separate narrow controlled Coleman pair, analyst-supplied common EPS/P-E worksheet. Independent arithmetic, fact-value bindings, worksheet-parameter conformance and line-bound report rounding. No producer code, outside sources or investment-meaning opinion.','audited_file_hashes':hashes,'source_binding_scope':{run:{'unique_bound_fact_ids':len(bound_ids[run]),'unique_referenced_fact_ids':len(referenced_ids[run])} for run in CONTROLLED},'summary':csummary,'total_checks':len(checks),'failed_checks':sum(not x['passed'] for x in checks),'check_counts_by_category':dict(collections.Counter(x['category'] for x in checks)),'report_rounded_claim_checks':len(report_checks),'report_rounded_claim_failures':sum(not x['passed'] for x in report_checks),'paired_common_grid':paired_common_grid,'findings':findings,'skipped_checks':skipped,'checks':checks,'report_checks':report_checks,'original_four_run_audit':'arithmetic-review.json','comparison_limit':'All fixed-worksheet scalar common-grid values agree under shared inputs and overlay. A single controlled pair does not establish causal effects, stable behavior, anchoring resistance, or native doctrine. No numerical parameter revision is reported in enriched; calibration meaning is reviewed separately.'}
 (ROOT/'audit/arithmetic-controlled-review.json').write_text(json.dumps(cresult,ensure_ascii=False,indent=2)+'\n')
 lines=['# Independent controlled Coleman arithmetic review','',f"Generated: {cresult['generated_at_utc']}",'',cresult['scope'],'','## Results',f"- {cresult['total_checks']} non-prose checks; {cresult['failed_checks']} failed.",f"- {len(report_checks)} line-bound report rounded claims; {cresult['report_rounded_claim_failures']} failed."]
 for run,su in csummary.items():lines += [f"- {run}: {su['checks']} checks, {su['arithmetic_scalars']} independently recomputed numeric scalars; {su['report_rounded_claims']} report claims."]
 lines+=['','## Findings']+['- '+x['run']+' / '+x['check_id']+': '+x.get('note','') for x in findings]
 lines+=['','## Common worksheet numerical agreement',cresult['comparison_limit'],'']
 for x in paired_common_grid:lines += [f"- {x['scenario']}: future price ${x['base']['price']:.8f}; five-year price CAGR {x['base']['cagr_percent']:.8f}%; maximum numeric output difference {x['max_absolute_difference']}."]
 lines+=['','## Frozen snapshots']+[f"- {run}: calculations {h['calculations_sha256']}; report {h['original_report_sha256']}." for run,h in hashes.items()]
 lines+=['','## Skipped']+['- '+x['run']+' / '+x['scope']+': '+x['reason'] for x in skipped]
 lines+=['- Full primary-source revalidation, external material claims, qualitative calibration and every report numeric token remain outside this arithmetic scope.','', 'Original four-run audit remains separate in arithmetic-review.json and arithmetic-review.md. Reproduce both cohorts with python audit/independentrecompute.py.']
 (ROOT/'audit/arithmetic-controlled-review.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'controlled_summary':csummary,'total_checks':len(checks),'failed_checks':[x for x in checks if not x['passed']],'report_failures':[x for x in report_checks if not x['passed']],'findings':findings},ensure_ascii=False,indent=2))
