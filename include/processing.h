#ifndef __PROCESSING_H__
#define __PROCESSING_H__


#include <vector>
#include <iostream>


using Track = std::vector<double>;


Track generate_centered_track(size_t nsamples);


double compute_mean(const std::vector<double> &track);
void center(std::vector<double> &track);
void apply_delay(std::vector<double> &track, size_t tau, double pan);
double cross_correlation(const std::vector<double> &track, size_t phi);


#endif
