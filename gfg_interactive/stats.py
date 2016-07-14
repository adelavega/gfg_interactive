def z2p(z):
    """
    from z-score return p-value
    """
    from math import erf, sqrt

    return 0.5 * (1 + erf(z / sqrt(2)))

def keep_track_turknorm(score):
	SAMPLE_MEAN = 0.74563218390804598
	SAMPLE_STD = 0.2842333722829018

	z_score = (score - SAMPLE_MEAN) / SAMPLE_STD

	return z2p(z_score)