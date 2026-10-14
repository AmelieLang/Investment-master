import json,math,hashlib,pathlib,datetime
p=pathlib.Path(__file__).resolve().parents[1]; f=p/'output/scenarios.json';d=json.loads(f.read_text()); checks=[]
def check(name,a,b):
 ok=math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-10); checks.append({'check':name,'recomputed':a,'reported':b,'pass':ok})
for k,s in d['scenarios'].items():
 r=d['facts']['ttm_revenue_usd_bn']; sh=d['projection_convention']['forecast_starting_diluted_share_proxy_bn']
 for i,(g,m,di,row) in enumerate(zip(s['revenue_growth_rates'],s['owner_net_income_margins'],s['forecast_diluted_share_growth_rates'],s['annual_projections'])):
  r*=1+g;sh*=1+di;ni=r*m;eps=ni/sh
  for n,v in [('revenue_usd_bn',r),('owner_attributable_net_income_usd_bn',ni),('forecast_diluted_shares_bn',sh),('forecast_eps_usd',eps)]:check(f'{k}.year{i+1}.{n}',v,row[n])
 price=eps*s['terminal_pe']; entry=d['facts']['entry_price_usd']; years=d['projection_convention']['holding_period_calendar_years']; hurdle=d['analyst_assumptions']['required_return']
 for n,v in [('future_share_price_usd',price),('price_only_cumulative_return',price/entry-1),('price_only_cagr',(price/entry)**(1/years)-1),('illustrative_present_required_return_hurdle_usd',price/(1+hurdle)**years)]:check(f'{k}.{n}',v,s[n])
check('ttm_margin',99.198/187.142,d['facts']['ttm_margin']);check('score_total',sum(x['score'] for x in d['self_designed_score']['components']),d['self_designed_score']['total'])
check('hurdle_target',entry*(1+hurdle)**years,d['analyst_assumptions']['required_future_price_to_meet_hurdle_usd'])
b=d['scenarios']['base']['annual_projections'][-1];ss=d['sensitivity_base_other_inputs_held_fixed']
for pe,v in zip(ss['terminal_pe_values'],ss['future_prices_for_pe_values']):check(f'pe_sensitivity_{pe}',b['forecast_eps_usd']*pe,v)
for m,v in zip(ss['terminal_net_margin_values'],ss['future_prices_for_margin_values']):check(f'margin_sensitivity_{m}',b['revenue_usd_bn']*m/b['forecast_diluted_shares_bn']*30,v)
check('dilution_sensitivity',b['owner_attributable_net_income_usd_bn']/(24.483*1.01**3)*30,ss['future_price_with_alternative_dilution'])
out={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'scope':'Arithmetic only, assumptions are not independently validated forecasts','checks':checks,'passed':all(x['pass'] for x in checks),'count':len(checks)}
(p/'audit/arithmetic-review.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'count':len(checks)}));assert out['passed']
