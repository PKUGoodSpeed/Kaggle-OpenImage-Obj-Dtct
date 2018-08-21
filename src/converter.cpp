#include <bits/stdc++.h>

using namespace std;
typedef vector<string> vs;

// const int N = 8466940;
const int N = 913354;

vs getToken(const string&s){
    vs ans;
    auto i = s.find_first_not_of(',');
    while(i<s.size() && i!=string::npos){
        auto j = s.find(",", i);
        if(j==string::npos) j = s.size();
        ans.push_back(s.substr(i, j-i));
        i = j+1;
    }
    return ans;
}

int main(int argc, char* argv[]){
    assert(argc > 2);
    std::ios_base::sync_with_stdio(false),cin.tie(0),cout.tie(0);
    freopen(argv[1], "r", stdin);
    string info;
    vector<vs> collect;
    cin>>info;
    string img_id = "";
    for(int i=0; i<N; ++i){
        cin>>info;
        cout<<info<<endl;
        vs tokens = getToken(info);
        if(tokens[0] == img_id){
            collect.push_back(tokens);
        }
        else{
            ofstream ofl;
            string filename = string(argv[2]) + "/" + img_id + ".txt";
            ofl.open(filename);
            for(vs &tks: collect){
                ofl << tks[1] << ' ' << tks[2] << ' ' << tks[3] << ' ' << tks[4] << ' ' << tks[5] <<endl;
            }
            collect.clear();
            img_id = tokens[0];
            collect.push_back(tokens);
        }
    }
    ofstream ofl;
    string filename = string(argv[2]) + "/" + img_id + ".txt";
    ofl.open(filename);
    for(vs &tks: collect){
        ofl << tks[1] << ' ' << tks[2] << ' ' << tks[3] << ' ' << tks[4] << ' ' << tks[5] <<endl;
    }
    return 0;
}