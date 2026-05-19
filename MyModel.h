#ifndef DNest4_Template_MyModel
#define DNest4_Template_MyModel

#include "DNest4/code/DNest4.h"
#include "MyConditionalPrior.h"
#include <ostream>

class MyModel
{
    private:
        // Static dataset
        static std::vector<int> home_teams;
        static std::vector<int> away_teams;
        static std::vector<double> home_team_win_margins;
        static void load_data();

    private:
        DNest4::RJObject<MyConditionalPrior> abilities;
        double s;     // Scale parameter for likelihood
        double nu;    // Shape parameter for likelihood

    public:
        // Constructor only gives size of params
        MyModel();

        // Generate the point from the prior
        void from_prior(DNest4::RNG& rng);

        // Metropolis-Hastings proposals
        double perturb(DNest4::RNG& rng);

        // Likelihood function
        double log_likelihood() const;

        // Print to stream
        void print(std::ostream& out) const;

        // Return string with column information
        std::string description() const;
};

#endif

