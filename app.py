from flask import Flask, render_template, request, redirect, url_for, flash
import csv, json, os, time
from algorithms import merge_sort, knapsack, dijkstra, nearest_neighbor
app = Flask(__name__)
app.secret_key = "mini-courier-demo-key"
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, "data", "parcels.csv")
GRAPH_FILE = os.path.join(ROOT, "data", "road_network.json")
REPORT_FILE = os.path.join(ROOT, "reports", "latest_plan.json")

def load_parcels():
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return [{**r, "weight":int(r["weight"]), "value":int(r["value"]), "priority":int(r["priority"])} for r in csv.DictReader(f)]

def save_parcels(items):
    with open(DATA_FILE,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["id","name","weight","value","priority"])
        w.writeheader(); w.writerows(items)

def load_graph():
    with open(GRAPH_FILE,encoding="utf-8") as f: return json.load(f)

@app.route("/", methods=["GET","POST"])
def index():
    parcels=load_parcels()
    capacity=20
    if request.method=="POST":
        action=request.form.get("action")
        if action=="add":
            try:
                name=request.form["name"].strip()
                weight=int(request.form["weight"]); value=int(request.form["value"]); priority=int(request.form["priority"])
                if not name or weight<=0 or value<0 or not 1<=priority<=5: raise ValueError()
                next_id=max([int(p["id"][1:]) for p in parcels]+[100])+1
                parcels.append({"id":f"P{next_id}","name":name,"weight":weight,"value":value,"priority":priority})
                save_parcels(parcels); flash("Parcel added successfully.","success")
            except (ValueError,KeyError): flash("Enter valid parcel details. Weight must be positive and priority 1–5.","error")
            return redirect(url_for("index"))
        if action=="delete":
            pid=request.form.get("parcel_id")
            parcels=[p for p in parcels if p["id"]!=pid]
            save_parcels(parcels); flash("Parcel deleted.","success")
            return redirect(url_for("index"))
        if action=="plan":
            try: capacity=int(request.form.get("capacity",20))
            except ValueError: capacity=20
            if capacity<0 or capacity>500: capacity=20
            t=time.perf_counter(); ordered=merge_sort(parcels); sort_ms=(time.perf_counter()-t)*1000
            t=time.perf_counter(); chosen,best=knapsack(ordered,capacity); pack_ms=(time.perf_counter()-t)*1000
            graph=load_graph()
            route,distance=nearest_neighbor(graph,"Depot")
            distances,_=dijkstra(graph,"Depot")
            result={"capacity":capacity,"ordered":ordered,"selected":chosen,"weight":sum(p["weight"] for p in chosen),
                    "value":best,"route":route,"distance":distance,"distances":distances,
                    "sort_ms":sort_ms,"pack_ms":pack_ms}
            os.makedirs(os.path.dirname(REPORT_FILE),exist_ok=True)
            with open(REPORT_FILE,"w",encoding="utf-8") as f: json.dump(result,f,indent=2)
            return render_template("index.html",parcels=parcels,result=result,capacity=capacity)
    return render_template("index.html",parcels=parcels,result=None,capacity=capacity)

if __name__=="__main__":
    app.run(host="127.0.0.1",port=5000,debug=False)
