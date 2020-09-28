#include<iostream>
#include<cstring>
#include<algorithm>
#include<fstream>
#include<math.h>
#include<algorithm>
#include<stack>
#include<queue>
using namespace std;
ifstream fin("edgelist_network2.txt");
ofstream outfile("result_network2.txt");
//streambuf *buf = cin.rdbuf(fin.rdbuf());//用于重定项输入改成，把cin当成fin


const float inf = 99999;
const int MAXN = 1000;
const int MAXM = 10000;

struct Node
{
    int s;
    int to;
    int next;
    int capacity;
    float value;
};

int n=100, m=3340;
int index;
Node node[MAXM];
int head[MAXN];
int pre[MAXN];
float dis[MAXN];
bool vis[MAXN];
int degree[MAXN];
float rel[100][100]={0};

void init()
{
    index = 0;
    memset(head, -1, sizeof(head));
    memset(node, 0, sizeof(node));
    memset(degree,0,sizeof(degree));
}
void addedge(int a, int b, float v, int c)
{
    node[index].to = b;
    node[index].s = a;
    node[index].value = v;
    node[index].capacity = c;
    node[index].next = head[a];
    head[a] = index++;

    node[index].to = a;
    node[index].s = b;
    node[index].value = -v;
    node[index].capacity = 0;
    node[index].next = head[b];
    head[b] = index++;
}

void deleteedge(int a,int b,int temp)
{
	index--;
	node[index].to = 0;
    node[index].s = 0;
    node[index].value = 0;
    node[index].capacity = 0;
    node[index].next = 0;
    head[a] = -1;
    index--;
    node[index].to = 0;
    node[index].s = 0;
    node[index].value = 0;
    node[index].capacity = 0;
    node[index].next = 0;
    head[b] = temp;

}

bool spfa(int s, int t, int nnum)
{
    memset(vis, 0, sizeof(vis));
    memset(pre, -1, sizeof(pre));
    for (int i = 0; i <= nnum; i++)
    {
        dis[i] = inf;
    }
    queue<int> que;
    que.push(s);
    dis[s] = 0;
    vis[s] = true;
    while (!que.empty())
    {
        int temp = que.front();
        que.pop();
        vis[temp] = false;
        //cout<<temp<<' '<<head[temp]<<endl;
        for (int i = head[temp]; i != -1; i = node[i].next)
        {
        	//cout<<i<<endl;
            if (node[i].capacity)
            {
                int ne = node[i].to;
                bool result = dis[temp] + node[i].value < dis[ne];
                //cout<<result<<endl;
                if (result)
                {
                    dis[ne] = dis[temp] + node[i].value;
                    pre[ne] = i;
                    if (!vis[ne])
                    {
                        vis[ne] = true;
                        que.push(ne);
                    }
                }
            }
        }
        //cout<<dis[t]<<endl;
    }
    if (dis[t] == inf)
        return false;
    return true;
}
float getMincost(int s, int t, int nnum)
{
    int ans_flow = 0;
    float ans_cost = 0;
    int temp, minc;
    while (spfa(s, t, nnum))
    {
    	//cout<<s<<" * "<<t<<endl;
        temp = t;
        minc = inf;
        while (pre[temp] != -1)
        {
            minc = min(node[pre[temp]].capacity, minc);
            temp = node[pre[temp]].s;
        }
        temp = t;
        while (pre[temp] != -1)
        {
            node[pre[temp]].capacity -= minc;
            int ss = pre[temp] ^ 1;
            node[ss].capacity += minc;
            temp = node[pre[temp]].s;
        }
        ans_cost += dis[t] * minc;
    }
    return ans_cost;
}
int main()
{
    int a, b;
    int s, t;
    float result,v;

    for(int i=1;i<=n;i++)
    	for(int j=i+1;j<=n;j++)
    	{
			init();
		    while(fin>>a>>b>>v)
		    {
		    	float temp = v*log2(1/v);
		    	//cout<<temp<<endl;
		        addedge(a, b, temp, 1);
		        addedge(b, a, temp, 1);
		        degree[a]++;
		        degree[b]++;

		    }
		    //cout<<"read once!"<<endl;
		    fin.clear();
		    fin.seekg(0,ios::beg);
    		s = n + 1;
    		t = s + 1;
    		//int temp_index_i=head[i],temp_index_j=head[j];
    		//int i = 1;
    		//int j = 6;
    		addedge(s, i, 0, degree[i]);
    		addedge(j, t, 0, degree[j]);
    		//cout<<"begin"<<endl;
    		result = getMincost(s,t,t);
    		cout<<i<<":"<<j<<" "<<result<<endl;
    		rel[i][j] = result;
    		rel[j][i] = result;
    		//deleteedge(s,i,temp_index_i);
    		//deleteedge(t,j,temp_index_j);
    	}

    //输出
    for(int i = 1;i<=n;i++)
    {
    	for(int j = 1;j<=n;j++)
    	{
    		outfile<<rel[i][j]<<' ';
    	}
    	outfile<<endl;
    }

    return 0;
}
