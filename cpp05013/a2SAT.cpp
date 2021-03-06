struct Graph{
    int n, cnt, sccnt; vector<vector<int>> adj;
    vector<int> up, visit, scx, stk;
    Graph(int n): n(n), adj(n+1), up(n+1), visit(n+1), scx(n+1) {}
    void connect(int a, int b){adj[a].push_back(b);}
    void dfs(int v){
        up[v] = visit[v] = ++cnt;
        stk.push_back(v);
        for(int nxt: adj[v]){
            if(!visit[nxt]) dfs(nxt), up[v] = min(up[v], up[nxt]);
            else if(!scx[nxt]) up[v] = min(up[v], visit[nxt]);
        }
        if(up[v] == visit[v]){
            ++sccnt; int t = -1;
            while(!stk.empty() && t != v){
                t = stk.back(); stk.pop_back();
                scx[t] = sccnt;
            }
        }
    }
    void getscc(){
        cnt = sccnt = 0;
        for(int i=1; i<=n; i++) if(!visit[i]) dfs(i);
    }
};

struct TwoSAT{
    int n; Graph G;
    TwoSAT(int var): n{var}, G{Graph(2*var+1)} {}
    int v(int x){return n+x+1;}
    void cnf(int x, int y){G.connect(v(-x),v(y)); G.connect(v(-y),v(x));}
    bool solve(){
        G.getscc();
        for(int x=1; x<=n; x++) if(G.scx[v(x)] == G.scx[v(-x)]) return false;
        return true;
    }
};