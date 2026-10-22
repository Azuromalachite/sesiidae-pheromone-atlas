import json, sys, statistics as st
rows=[json.loads(l) for l in open(sys.argv[1]) if '"c18|' in l]
for rule in ("nearest_nucleus","radius_scaled"):
    print("rule", rule, "(n=%d conformers)"%len(rows))
    print("  pair      meanDiff  pairedSD  pairedMin..Max   sign-consistent  |  site range a, b")
    for c in list(range(1,6))+list(range(10,18)):
        a,b=f"C{c+3}",f"C{c+4}"
        d=[r["sites"][rule][a]["V_area_mean"]-r["sites"][rule][b]["V_area_mean"] for r in rows]
        ra=[r["sites"][rule][a]["V_area_mean"] for r in rows]; rb=[r["sites"][rule][b]["V_area_mean"] for r in rows]
        same=max(sum(x>0 for x in d), sum(x<0 for x in d))
        print(f"  C{c}-C{c+1:<3} {st.mean(d):8.2f} {st.stdev(d):8.2f}  {min(d):6.2f}..{max(d):6.2f}   {same}/10        |  {max(ra)-min(ra):5.2f} {max(rb)-min(rb):5.2f}")
