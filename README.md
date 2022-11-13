This is a broad framework for the following technical session. If you have questions, you can reach me on (in order of responsiveness) [Discord](matteoettam09#9362), [LinkedIn](https://www.linkedin.com/in/matteomanzi00seinfeldwasright/), [email](matteo.manzi@crunchdao.com). Please schedule a call selecting one slot from [this link](https://calendly.com/matteoettam09/coffee-with-matteo-crunchdao).

# Dimensionality Reduction

CrunchDAO receives hundreds of predictions every week coming from the DAO members participating in the supervised learning problem of the tournament.

The first step of the pipeline, *before* ensamble learning, is dimensionality reduction/clustering.
In out technical call we will discuss:

- [this work](https://www.researchgate.net/publication/363573709_Machine_Learning_Methods_for_Nonlinear_Reduced-order_Modeling_of_the_Thermospheric_Density_Field).
- K-means clustering, Kernel K-means clustering, hierarchical clustering.

Imagine you have a week after which you have to select the algorithm to put in production. All you have are the submissions (every week different number of submissions) to the tournament. You can assume the dimensionality of the prediction vector to be constant across epochs.

How do you plan that week?

# Convex Optimizer-in-the-loop backpropagation

There is a black box model: the input is a set of weights and a set of vectors. Everything is condensated with an analytical/analytically approximated function into a few vectors (1-3), input of a [convex optimizer](https://www.cvxpy.org/) with analytical fitness and constraints. A numerical fitness is associated with the ouput of the convex optimizer. Let's compute the gradient of such fitness with respect to the intial weights.
See the following resources:

- [Differentiable Convex Optimization Layers](https://web.stanford.edu/~boyd/papers/pdf/diff_cvxpy.pdf)
- [True Contribution](https://docs.numer.ai/tournament/true-contribution-tc)

# Dynamical Systems

You have a discrete dynamical system (e.g., the standard map presented in [this paper](https://raw.githubusercontent.com/JuliaCon/proceedings-papers/jcon.00111/jcon.00111/10.21105.jcon.00111.pdf)). Do not base your considerations on the analytical knowledge of the model. You have an estimate of the initial condition statistics. Can you qualitatively characterize the long term behaviours of such system? 

  After the state propagation, we compute an analytical function of the final state. We are interested in the ratio between its expectation and its standard deviation (see [here](https://en.wikipedia.org/wiki/Sharpe_ratio)). How can we compute it efficiently?
