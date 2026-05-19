#include "MyConditionalPrior.h"
#include "DNest4/code/DNest4.h"
#include <cmath>

MyConditionalPrior::MyConditionalPrior()
{

}

void MyConditionalPrior::from_prior(DNest4::RNG& rng)
{
    sigma = exp(log(0.1) + log(1E3)*rng.rand());
}

double MyConditionalPrior::perturb_hyperparameters(DNest4::RNG& rng)
{
    double logH = 0.0;

    sigma = log(sigma);
    sigma += log(1E3)*rng.randh();
    DNest4::wrap(sigma, log(0.1), log(1E2));
    sigma = exp(sigma);

    return logH;
}

double MyConditionalPrior::log_pdf(const std::vector<double>& vec) const
{
    double logp = 0.0;

    DNest4::Laplace l(0.0, sigma);
    for(double ability: vec)
        logp += l.log_pdf(ability);

    return logp;
}

void MyConditionalPrior::from_uniform(std::vector<double>& vec) const
{
    DNest4::Laplace l(0.0, sigma);
    for(size_t i=0; i<vec.size(); ++i)
        vec[i] = l.cdf_inverse(vec[i]);
}

void MyConditionalPrior::to_uniform(std::vector<double>& vec) const
{
    DNest4::Laplace l(0.0, sigma);
    for(size_t i=0; i<vec.size(); ++i)
        vec[i] = l.cdf(vec[i]);
}

void MyConditionalPrior::print(std::ostream& out) const
{
    out<<sigma<<' ';
}

