#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
using namespace std;

const vector<char> letters = {'V', 'E', 'R', 'Y', 'H', 'A', 'D', 'I', 'S', 'T'};
const string LHS[3] = {"VERY", "HARD", "IS"};
const string RHS = "THIS";


unordered_map<char, int> lettersToInt; //hashmap that maps all 10 chars V,E,R ... to a unique integer from 0-9

vector<bool> visited(10, false); //tracks if all 10 letters have been used, then and only then will isSolved be ran, i.e a permuation is generated if all values in visited are true


//this function is ran everytime a permuation (each letter assigned to a unique integer) is generated
//iterates through each string within the LHS of the eqn and computes a total sum, then subtracts the integer value from the RHS, returns true if the LHS-RHS = 0, false otherwise
bool isSolved()
{
    int sum = 0;
    int res = 0;
    for (const string &str : LHS)
    {
        res = 0;
        for (char c : str)
        {
            res = res * 10 + lettersToInt[c];
        }
        sum += res;
    }
    res = 0;
    for (char c : RHS)
    {
        res = res * 10 + lettersToInt[c];
    }
    sum -= res;
    return sum == 0;
}

//utilizes recursion with backtracking to generate every possible permutation of char to integer mappings
void solve(int currLetter)
{
    //check every letter has been visited
    if (currLetter == letters.size())
    {
        //if a given lettersToInt mapping is correct, print out the values and exit
        if (isSolved())
        {
            for(const string& str: LHS){
                cout<<str<<"(";
                for(char c: str){
                    cout<<lettersToInt[c];
                }
                cout<<")"<<" ";
            }
            cout<<"| "<<RHS<<"(";
            for(char c: RHS){
                cout<<lettersToInt[c];
            }
            cout<<")"<<"\n";
            exit(0);
        }
        return;
    }
    
    for (int i = 0; i < 10; i++)
    {
        //if a value from 0-9 has not been mapped, i.e the integer is not being used
        if (!visited[i])
        {
            //map the current char to that value
            visited[i] = true; 
            lettersToInt[letters[currLetter]] = i;
            solve(currLetter + 1); //recursive call to next letter
            visited[i] = false; //reset for backtracking
        }
    }
}
int main()
{
    solve(0);
    cout<<"No solution found"<<"\n";
    return 0;
}
