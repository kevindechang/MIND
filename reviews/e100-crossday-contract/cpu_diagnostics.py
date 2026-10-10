"""Optional processor-time calibration: not the frozen primary cost estimand."""
import json
import statistics
import time
from dynamic_probe import Base,Eager,Lazy,generate

classes={'graph':Base,'eager':Eager,'lazy':Lazy}
rows={}
for p in (0.2,0.8):
    for density in (0.1,0.4):
        k=f'q{p}_d{density}'
        totals={name:[] for name in classes}
        for repeat in range(5):
            for seed in range(10000,10032):
                edges,events=generate(seed,density,p)
                names=list(classes)
                names=names[(seed+repeat)%3:]+names[:(seed+repeat)%3]
                for name in names:
                    start=time.process_time_ns()
                    model=classes[name](edges)
                    for event in events:
                        if event['type']=='query': model.act(event['goal'])
                        else: model.public_update(event)
                    totals[name].append(time.process_time_ns()-start)
        rows[k]={name:{'median_cpu_ns_per_180_events':round(statistics.median(v)),
                       'min_max_cpu_ns':[min(v),max(v)],'runs':len(v)} for name,v in totals.items()}
print(json.dumps({'status':'PASS','measurement':'process_time_ns CPU on this host; warmup/order effects possible; no true hardware parity', 'strata':rows},indent=2,sort_keys=True))
