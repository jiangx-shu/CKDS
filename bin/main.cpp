#include <iostream>
#include <fstream>
#include <cstring>
#include <cmath>
#include <algorithm>

#define MAXN 100
#define MAXM 100

using namespace std;
    int net1_matrix[MAXN][MAXN],net2_matrix[MAXN][MAXN],graphlet_diff[MAXN][15];
    int graphlet1[MAXN][15],graphlet2[MAXN][15];
    int mapping[MAXN][2];
    int oi[15]={1, 2, 1, 3, 2, 2, 2, 1, 3, 1, 2, 2, 2, 1, 4};
    float omigai[15],diff[MAXN];
    float similarity[MAXN],sim;

//Read the edge set of the network1
ifstream net1_in("network1.txt");
//Read the edge set of the network2
ifstream net2_in("network2.txt");
//Output the network graphlet to files
ofstream net1_out("network1_graphlet.txt");
ofstream net2_out("network2_graphlet.txt");

//Read the graphlet vector of network 1 and 2
ifstream graphlet1_in("network1_graphlet.txt");
ifstream graphlet2_in("network2_graphlet.txt");
//Output the graphlet D-value to files
ofstream diff_out("graphlet_diff.txt");
ofstream dvalue_out("graphlet_dvalue.txt");

//Input the node number mappings of the two network

//Read the edge set of the network1
//ifstream net1_in("test_state1_net_1.txt");
////Read the edge set of the network2
//ifstream net2_in("test_state2_net_2.txt");
////Output the network graphlet to files
//ofstream net1_out("test_state1_graphlet.txt");
//ofstream net2_out("test_state2_graphlet.txt");
//
////Read the graphlet vector of network 1 and 2
//ifstream graphlet1_in("test_state1_graphlet.txt");
//ifstream graphlet2_in("test_state2_graphlet.txt");
////Output the graphlet D-value to files
//ofstream diff_out("test_diff.txt");
//ofstream dvalue_out("test_dvalue.txt");
//
////Input the node number mappings of the two network
//ifstream nMap_in("test_node_mapping.txt");

//Comput graphlet of the adjacency matrix
void graphlet_vector(int net_matrix[MAXN][MAXN],int len,int graphlet[MAXN][15])
{
    int i,j,k,h;
    //2-node graphlet
    for(i=0;i<len;i++)
    {
        for(j=0;j<len;j++)
        {
            if(j==i){continue;}
            if(j<len)
            {
                if(net_matrix[i][j])
                    graphlet[i][0]++;
            }
        }
    }
    //end 2-node graphlet

    //3-node graphlet
    for(i=0;i<len;i++)
    {
        for(j=0;j<len;j++)
        {
            if(i==j){continue;}
            for(k=0;k<len;k++)
            {
                if(k==i||k==j)
                {
                    continue;
                }
                if(net_matrix[i][j]&&net_matrix[i][k]&&net_matrix[j][k]){
                    graphlet[i][3]++;
                }
                else if(net_matrix[i][j]&&!net_matrix[i][k]&&net_matrix[j][k])
                {
                    graphlet[i][1]++;
                }
                else if(net_matrix[i][j]&&net_matrix[i][k]&&!net_matrix[j][k])
                {
                    graphlet[i][2]++;
                }
				//cout<<i<<" "<<j<<" "<<k<<" "<<endl;
            }
        }
        graphlet[i][2]/=2;
        graphlet[i][3]/=2;
    }
    //end 3-node graphlet

    //4-node graphlet
    for(i=0;i<len;i++)
    {
        for(j=0;j<len;j++)
        {
            if(j==i) {continue;}
            for(k=0;k<len;k++)
            {
                if(k==i) continue;
                if(k==j) continue;
                for(h=0;h<len;h++)
                {
                    if(h==i) continue;
                    if(h==j) continue;
                    if(h==k) continue;
                    int cnt = net_matrix[i][j]+net_matrix[i][k]+net_matrix[i][h]+net_matrix[j][k]+net_matrix[j][h]+net_matrix[k][h];
                    if(net_matrix[i][j]&&net_matrix[j][k]&&net_matrix[k][h]&&cnt==3)
                        graphlet[i][4]++;
                    if(net_matrix[i][j]&&net_matrix[i][k]&&net_matrix[k][h]&&cnt==3)
                        graphlet[i][5]++;
                    if(net_matrix[i][j]&&net_matrix[j][k]&&net_matrix[j][h]&&cnt==3)
                    {
                        graphlet[i][6]++;
                    }
                    if(net_matrix[i][j]&&net_matrix[i][k]&&net_matrix[i][h]&&cnt==3)
                    {
                        graphlet[i][7]++;
                    }
                    if(net_matrix[i][j]&&net_matrix[j][k]&&net_matrix[k][h]&&net_matrix[h][i]&&cnt==4)
                    {
                        graphlet[i][8]++;
                    }
                    if(net_matrix[i][j]&&net_matrix[i][k]&&net_matrix[j][k]&&net_matrix[k][h]&&cnt==4)
                    {
                        graphlet[i][9]++;
                    }
                    if(net_matrix[i][j]&&net_matrix[i][k]&&net_matrix[j][k]&&net_matrix[i][h]&&cnt==4)
                        graphlet[i][10]++;
                    if(net_matrix[i][j]&&net_matrix[j][k]&&net_matrix[j][h]&&net_matrix[k][h]&&cnt==4)
                    {
                        graphlet[i][11]++;
                    }
                    if(net_matrix[i][j]&&net_matrix[i][k]&&net_matrix[j][k]&&net_matrix[i][h]&&net_matrix[j][h]&&cnt==5)
                    {
                        graphlet[i][12]++;
                    }
                    if(net_matrix[i][k]&&net_matrix[i][h]&&net_matrix[j][k]&&net_matrix[j][h]&&net_matrix[k][h]&&cnt==5)
                        graphlet[i][13]++;
                    if(cnt==6)
                    {
                        graphlet[i][14]++;
                    }
                }
            }
        }
        graphlet[i][6]/=2;
        graphlet[i][7]/=6;
        graphlet[i][8]/=2;
        graphlet[i][10]/=2;
        graphlet[i][11]/=2;
        graphlet[i][12]/=2;
        graphlet[i][13]/=2;
        graphlet[i][14]/=6;
        cout<<i<<endl;
    }

    //end 4-node graphlet

}

//º∆À„∏˜∏ˆÕº‘™µƒ»®÷µ
void omiga_compute(int oi[],float omiga[])
{
    for(int i=0;i<15;i++)
    {
        omiga[i] = 1-(log10(oi[i])/log10(15));
    }
}

//º∆À„∏˜∏ˆΩ⁄µ„≤Ó“Ï∂»
void pair_diff(int graphlet1[MAXN][15],int graphlet2[MAXN][15],float omigai[],float diff[MAXN])
{
    int i,j;
    float sigma;
    float omiga=0.00;
    for(i=0;i<15;i++)
        omiga+=omigai[i];
    for(i=0;i<MAXN;i++)
    {
        sigma=0.00;
        for(j=0;j<15;j++)
        {
            sigma += omigai[j]*abs(log2(graphlet1[i][j]+1)-log2(graphlet2[i][j]+1))/(log2(max(graphlet1[i][j],graphlet2[i][j])+2));
        }
        diff[i]=sigma/omiga;
    }
}

int main()
{

    memset(net1_matrix,0,sizeof(net1_matrix));
    memset(graphlet1,0,sizeof(graphlet1));
    memset(net2_matrix,0,sizeof(net2_matrix));
    memset(graphlet2,0,sizeof(graphlet2));
    memset(omigai,0.0,sizeof(omigai));
    memset(diff,0.0,sizeof(diff));
    memset(similarity,0.0,sizeof(similarity));
    memset(mapping,0,sizeof(mapping));

    int edge1,edge2,simi;
    //Input edge sets and transfer into adjacency matrix
    while(!net1_in.eof())
    {
        net1_in>>edge1>>edge2;
        net1_matrix[edge1][edge2]=net1_matrix[edge2][edge1]=1;
    }

    while(!net2_in.eof())
    {
        net2_in>>edge1>>edge2;
        net2_matrix[edge1][edge2]=net2_matrix[edge2][edge1]=1;
    }



    graphlet_vector(net1_matrix,MAXN,graphlet1);
    graphlet_vector(net2_matrix,MAXM,graphlet2);



    int p,q;
    for(p=0;p<MAXN;p++)
    {
        for(q=0;q<15;q++)
        {
            net1_out<<graphlet1[p][q]<<" ";
        }
        net1_out<<endl;
    }
    for(p=0;p<MAXM;p++)
    {
        for(q=0;q<15;q++)
        {
            net2_out<<graphlet2[p][q]<<" ";
        }
        net2_out<<endl;
    }
    //º∆À„¡Ω∏ˆÕ¯¬ÁÕº‘™µƒ≤ÓœÚ¡ø
//    graphlet_D_value(graphlet1,graphlet2,graphlet_diff);
    for(int k1=0;k1<MAXN;k1++)
    {
        for(int k2=0;k2<15;k2++)
        {
            graphlet_diff[k1][k2]=graphlet1[k1][k2]-graphlet2[k1][k2];
        }
    }


    for(p=0;p<MAXN;p++)
    {
        for(q=0;q<15;q++)
        {
            diff_out<<graphlet_diff[p][q]<<" ";
        }
        diff_out<<endl;
    }
    cout<<"Caculate finished.\nThe result was written in the file \"./graphlet_diff.txt\"."<<endl;


    //º∆À„Õº‘™œÚ¡ø≤Ó“Ï∂»
    omiga_compute(oi,omigai);
    pair_diff(graphlet1,graphlet2,omigai,diff);
    for(int r=0;r<MAXN;r++)
    {
        dvalue_out<<r<<"\t"<<diff[r]<<endl;
    }
    return 0;
}
