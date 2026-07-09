import os, json, urllib.request, datetime
KEY = os.environ["METABASE_KEY"]
row = json.load(urllib.request.urlopen(urllib.request.Request(
    "https://metabase.wiom.in/api/card/11522/query/json", data=b"{}",
    headers={"x-api-key": KEY, "Content-Type": "application/json"})))[0]
G = lambda k: int(row[k])
tot=G('TOTAL');H=G('HEALTHY');PO=G('PAID_OFFLINE');NPO=G('NOTPAID_ONLINE');CO=G('CORRECTLY_OFF')
onus=G('ON_US');onp=G('ON_PARTNER');dev=G('DEVICE_OFF');leak=G('NP_LEAK_30D');left=G('NP_LEFTOVER');mh=G('MONEY_HEALTHY');mt=G('MONEY_TAIL')
pc = lambda x: '%.1f%%' % (100*x/tot)
def L(cid,val,col): return '<a href="https://metabase.wiom.in/question/%d" target="_blank" style="color:%s;font-weight:700;text-decoration:underline">%s &#8595;</a>'%(cid,col,format(val,','))
css="""*{box-sizing:border-box}body{margin:0;background:#0f1720;color:#e7edf3;font-family:-apple-system,Segoe UI,Arial,sans-serif;font-size:14px}
.top{padding:18px 26px;border-bottom:1px solid #243342;display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px}
.top h1{margin:0;font-size:20px}.top .sub{color:#8aa0b4;font-size:12.5px}
.wrap{padding:22px 26px;max-width:1100px}
.axis{display:grid;grid-template-columns:110px 1fr 1fr;gap:12px}
.axhead,.rowlbl{display:flex;align-items:center;justify-content:center;color:#8aa0b4;font-size:12px;text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.box{background:#17212b;border:1px solid #243342;border-radius:12px;padding:18px 20px;min-height:130px}
.box .tag{font-size:12px;text-transform:uppercase;letter-spacing:.05em;font-weight:700}.box .val{font-size:38px;font-weight:800;margin:6px 0 2px;line-height:1}
.box .pct{color:#8aa0b4;font-size:12.5px}.box .desc{font-size:12.5px;margin-top:10px;color:#8aa0b4}
.box.green{border-color:#245c3a}.box.green .tag{color:#4ade80}.box.red{border-color:#6b2529}.box.red .tag{color:#ff6b70}.box.red .val{color:#ff6b70}
.box.amber{border-color:#6b551a}.box.amber .tag{color:#f0b429}.box.grey .tag{color:#8aa0b4}
h2{font-size:13px;color:#8aa0b4;text-transform:uppercase;letter-spacing:.05em;margin:26px 0 10px;border-bottom:1px solid #243342;padding-bottom:6px}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px}.rc{background:#17212b;border:1px solid #243342;border-radius:10px;padding:16px}.rc h3{margin:0 0 12px;font-size:14px}
.li{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #243342;font-size:13px;gap:12px}.li:last-child{border:none}.li .n{font-weight:700}
.n.mut{color:#8aa0b4}.n.amber{color:#f0b429}
.money{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.m{background:#17212b;border:1px solid #243342;border-radius:10px;padding:14px 16px}.m .l{color:#8aa0b4;font-size:11.5px}.m .v{font-size:22px;font-weight:700;margin-top:4px}
.note{color:#8aa0b4;font-size:12px;margin-top:18px;line-height:1.55}
@media(max-width:640px){.axis,.cards,.money{grid-template-columns:1fr}}"""
h=[]
h.append('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RDNI Dashboard</title><style>'+css+'</style></head><body>')
h.append('<div class="top"><div><h1>RDNI Dashboard &mdash; Recharge Done, No Internet</h1><div class="sub">Is every paying customer online, and are we paying the ISP partner for the right customers?</div></div>')
h.append('<div class="sub">%s customers &middot; updated %s IST &middot; <span style="color:#1f9d55">&#9679; auto-refreshed daily</span></div></div>'%(format(tot,','),(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=5,minutes=30)).strftime('%d %b %Y %H:%M')))
h.append('<div class="wrap"><div class="axis"><div></div><div class="axhead">Online</div><div class="axhead">Offline</div>')
h.append('<div class="rowlbl">Paid</div>')
h.append('<div class="box green"><div class="tag">Healthy</div><div class="val">%s</div><div class="pct">%s</div><div class="desc">Paying and online.</div></div>'%(format(H,','),pc(H)))
h.append('<div class="box red"><div class="tag">Paid but offline</div><div class="val">%s</div><div class="pct">%s</div><div class="desc">Paying, not online right now.</div></div>'%(format(PO,','),pc(PO)))
h.append('<div class="rowlbl">Not paid</div>')
h.append('<div class="box amber"><div class="tag">Not paid but online</div><div class="val">%s</div><div class="pct">%s</div><div class="desc">Online without a live plan.</div></div>'%(format(NPO,','),pc(NPO)))
h.append('<div class="box grey"><div class="tag">Correctly off</div><div class="val">%s</div><div class="pct">%s</div><div class="desc">Not paying, not online.</div></div></div>'%(format(CO,','),pc(CO)))
h.append('<h2>What needs action</h2><div class="cards">')
h.append('<div class="rc"><h3>Paid but offline &mdash; %s &nbsp;<span style="color:#8aa0b4;font-size:11px">who owns the fix?</span></h3>'%format(PO,','))
h.append('<div class="li"><span><b>On us</b> &mdash; no ISP ticket raised / plan not migrated</span><span>%s</span></div>'%L(11524,onus,'#ff6b70'))
h.append('<div class="li"><span><b>On partner</b> &mdash; ISP ticket raised, ISP not restored</span><span>%s</span></div>'%L(11525,onp,'#f0b429'))
h.append('<div class="li"><span>Router off &mdash; plan &amp; ISP fine on our side</span><span class="n mut">%s</span></div></div>'%format(dev,','))
h.append('<div class="rc"><h3>Not paid but online &mdash; %s</h3>'%format(NPO,','))
h.append('<div class="li"><span>Leftover ISP coverage &mdash; expires soon</span><span class="n mut">%s</span></div>'%format(left,','))
h.append('<div class="li"><span><b>Online 30+ days after plan ended</b> &mdash; free usage</span><span class="n amber">%s</span></div></div></div>'%format(leak,','))
h.append('<h2>ISP commission &mdash; are we paying for the right customers?</h2><div class="money">')
h.append('<div class="m"><div class="l">Paid for a paying, online customer</div><div class="v" style="color:#4ade80">%s</div></div>'%format(mh,','))
h.append('<div class="m"><div class="l">Paid for lapsed / offline (coverage tail)</div><div class="v" style="color:#f0b429">%s</div></div>'%format(mt,','))
h.append('<div class="m"><div class="l">Redundant tickets (over-buying)</div><div class="v" style="color:#4ade80">0</div></div></div>')
h.append('<div class="note"><b>Paid</b> = plan valid today (TRUM). <b>Online</b> = device seen in last 24h. Click <b>On us</b> or <b>On partner</b> to open the customer list and export CSV (Wiom login). Auto-refreshes daily.</div></div></body></html>')
open('index.html','w',encoding='utf-8').write('\n'.join(h))
print('index.html regenerated')
