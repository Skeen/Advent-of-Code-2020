#include <iostream>
#include <fstream>
#include <algorithm>
#include <iterator>
#include <vector>

int main()
{
    std::vector<int> integers;
    std::ifstream inputFile("input");
    std::istream_iterator<int> input(inputFile);
    std::copy(input, std::istream_iterator<int>(), std::back_inserter(integers));

    for(int i : integers)
    {
        for(int j : integers)
        {
            for(int k : integers)
            {
                int sum = i + j + k;
                if (sum == 2020) {
                    std::cout << i * j * k << std::endl;
                    exit(0);
                }
            }
        }
    }
}
