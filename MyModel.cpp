#include "MyModel.h"
#include "DNest4/code/DNest4.h"
#include <fstream>

std::vector<int> MyModel::home_teams;
std::vector<int> MyModel::away_teams;
std::vector<double> MyModel::home_team_win_margins;
std::set<int> MyModel::teams;
int MyModel::num_teams = 0;

void MyModel::load_data()
{
    std::fstream fin("matches.txt", std::ios::in);

    // Skip header
    std::string header;
    std::getline(fin, header);

    int round, home_team, away_team, home_score, away_score;
    while(fin >> round && fin >> home_team && fin >> away_team &&
          fin >> home_score && fin >> away_score)
    {
        home_teams.push_back(home_team);
        away_teams.push_back(away_team);
        double margin = home_score - away_score;
        home_team_win_margins.push_back(margin);
        teams.insert(home_team);
        teams.insert(away_team);
    }

    fin.close();

    num_teams = teams.size();
    std::cout << "# Read " << home_teams.size() << " matches." << std::endl;
    std::cout << "# Detected " << num_teams << " teams." << std::endl;
}

MyModel::MyModel()
:abilities(1, num_teams, true, MyConditionalPrior())
{

}

void MyModel::from_prior(DNest4::RNG& rng)
{
    abilities.from_prior(rng);
    home_bonus = 2.0*tan(M_PI*(rng.rand() - 0.5));
    s  = exp(log(0.1) + log(1E3)*rng.rand());
    nu = exp(log(0.1) + log(1E3)*rng.rand());
}

double MyModel::perturb(DNest4::RNG& rng)
{
    double logH = 0.;

    if(rng.rand() <= 0.5)
        logH += abilities.perturb(rng);

    int which = rng.rand_int(3);
    if(which == 0)
    {
        home_bonus = atan(home_bonus/2.0)/M_PI + 0.5;
        home_bonus += rng.randh();
        DNest4::wrap(home_bonus, 0.0, 1.0);
        home_bonus = 2.0*tan(M_PI*(home_bonus - 0.5));
    }
    else if(which == 1)
    {
        s = log(s);
        s += log(1E3)*rng.randh();
        DNest4::wrap(s, log(0.1), log(1E2));
        s = exp(s);
    }
    else
    {
        nu = log(nu);
        nu += log(1E3)*rng.randh();
        DNest4::wrap(nu, log(0.1), log(1E2));
        nu = exp(nu);
    }

    return logH;
}

double MyModel::log_likelihood() const
{
    double logL = 0.0;

    double ssq = s*s;
    const auto& as = abilities.get_components();
    for(size_t i=0; i<home_teams.size(); ++i)
    {
        double& y = home_team_win_margins[i];
        double mu = home_bonus + as[home_teams[i]][0] - as[away_teams[i]][0];
		logL += std::lgamma(0.5*(nu + 1.0)) - std::lgamma(0.5*nu)
			        -0.5*log(M_PI*nu) -0.5*log(ssq)
        			-0.5*(nu + 1.0)*log(1.0 + pow(y - mu, 2)/ssq/nu);
    }

    return logL;
}

void MyModel::print(std::ostream& out) const
{
    out << home_bonus << ' ' << nu << ' ' << s << ' ';
    abilities.print(out);
}

std::string MyModel::description() const
{
    return std::string("");
}

