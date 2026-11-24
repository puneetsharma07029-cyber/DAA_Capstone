import heapq
def merge_sort(items):
    if len(items)<=1: return items[:]
    m=len(items)//2; a=merge_sort(items[:m]); b=merge_sort(items[m:])
    out=[]; i=j=0
    while i<len(a) and j<len(b):
        if (a[i]["priority"],a[i]["value"]) >= (b[j]["priority"],b[j]["value"]):
            out.append(a[i]); i+=1
        else: out.append(b[j]); j+=1
    return out+a[i:]+b[j:]
def knapsack(items,capacity):
    n=len(items); dp=[[0]*(capacity+1) for _ in range(n+1)]
    for i,p in enumerate(items,1):
        for c in range(capacity+1):
            dp[i][c]=dp[i-1][c]
            if p["weight"]<=c:
                dp[i][c]=max(dp[i][c],p["value"]+dp[i-1][c-p["weight"]])
    chosen=[]; c=capacity
    for i in range(n,0,-1):
        if dp[i][c]!=dp[i-1][c]:
            chosen.append(items[i-1]); c-=items[i-1]["weight"]
    return chosen[::-1],dp[n][capacity]
def dijkstra(graph,start):
    dist={v:float("inf") for v in graph}; prev={v:None for v in graph}; dist[start]=0
    q=[(0,start)]
    while q:
        d,u=heapq.heappop(q)
        if d!=dist[u]: continue
        for v,w in graph[u].items():
            nd=d+w
            if nd<dist[v]: dist[v]=nd; prev[v]=u; heapq.heappush(q,(nd,v))
    return dist,prev
def nearest_neighbor(graph,start):
    left=set(graph)-{start}; route=[start]; total=0; cur=start
    while left:
        options=[(graph[cur][v],v) for v in left if v in graph[cur]]
        if not options: break
        w,nxt=min(options); total+=w; route.append(nxt); left.remove(nxt); cur=nxt
    if start in graph[cur]: total+=graph[cur][start]; route.append(start)
    return route,total
