# Why a body with many contacts only needs a 6횞6 factorization

The force solver still solves

$$
(D + JWJ^\top)f = r.
$$

If a body has $d$ contact incidences, this equation has $3d$ unknowns.
Woodbury reduction is a way to solve that same equation using diagonal
operations, a small 6횞6 factorization, and a reconstruction of all $3d$
force components. It does not approximate the contact forces or replace them
with a single resultant wrench.

This note derives the reduction from the original equation and connects it
to stacking-core's CPU and GPU implementations.

## 1. Start with the variables we already have

Consider one rigid body in 3D. Each contact incidence contributes a force
vector with two tangential components and one normal component. Stack them:

$$
f =
\begin{bmatrix}
f_1\\ f_2\\ \vdots\\ f_d
\end{bmatrix}
\in \mathbb R^{3d}.
$$

An *incidence* means one body's participation in a contact. A ground contact
has one incidence; a pair contact has two, one for each body. Graph ADMM stores
one local force copy per incidence and enforces agreement between pair copies.

For this body, the relevant quantities are:

| Symbol | Size | Meaning |
| --- | --- | --- |
| $f$ | $3d$ | All body-local contact force components |
| $J$ | $3d\times6$ | Stacked contact Jacobian |
| $J^\top f$ | $6$ | Resultant contact wrench on this body |
| $W$ | $6\times6$ | Weight on the body's wrench error |
| $D$ | $3d\times3d$, diagonal | Regularization and ADMM penalties |
| $r$ | $3d$ | Right-hand side of this ADMM body update |

A rigid-body wrench has six components: three for force and three for torque.
Thus, regardless of how many contacts exist, their resultant wrench has only
six components.

The Jacobian convention is important: $J$ maps a body twist to contact
velocities, and its transpose maps contact forces to a body wrench. For a
single contact with lever arm $\ell$, expressed in a common frame, the
kinematic contribution is

$$
u = v + \omega\times\ell
  = \begin{bmatrix}I_3 & -[\ell]_\times\end{bmatrix}
    \begin{bmatrix}v\\\omega\end{bmatrix}.
$$

Taking the transpose gives the familiar wrench
$[f;\,\ell\times f]$. Contact-frame rotations and pair-side signs are
included in the actual stored Jacobians.

## 2. Where does the matrix come from?

At fixed poses and fixed ADMM auxiliary/dual variables, the body's force
update is an unconstrained quadratic minimization. Here, assume that $W$
is symmetric, as intended for a quadratic wrench-error weight. A schematic form is

$$
\min_f\quad
\frac12(J^\top f+w_{\mathrm{ext}})^\top
W(J^\top f+w_{\mathrm{ext}})
+\frac12 f^\top Df-b^\top f.
$$

Here, $w_{\mathrm{ext}}$ includes the mass-normalized gravity wrench.
Terms constant with respect to $f$ can be ignored during this update.

Differentiating with respect to $f$ gives

$$
JW(J^\top f+w_{\mathrm{ext}})+Df-b=0,
$$

so

$$
(D+JWJ^\top)f=r,
\qquad r=b-JWw_{\mathrm{ext}}.
$$

In the current implementation, the diagonal entry for a force coordinate is

$$
D_{kk} = \rho
+\mathbf{1}_{\text{candidate body}}\,k_{\mathrm{comp}}
  \max(\mathrm{gap}-\epsilon_{\mathrm{comp}},0)^2
+\beta_{\mathrm{contact}}
+\mathbf{1}_{\text{pair contact}}\,\beta_{\mathrm{consensus}}.
$$

The linear term $b$ contains the current auxiliaries, representatives, and
unscaled ADMM duals. Those change during the iterations.

**The cone constraints are handled by a separate ADMM projection step.**
The body update above is only one phase of the constrained force solve.
Woodbury reduction applies to this quadratic phase; it does not solve the
entire cone-constrained problem in one linear solve.

## 3. The structure hidden inside the large matrix

Write the Jacobian as a stack of contact blocks:

$$
J=\begin{bmatrix}J_1\\J_2\\\vdots\\J_d\end{bmatrix},
\qquad J_e\in\mathbb R^{3\times6}.
$$

The $(e,h)$ contact block of the dense coupling matrix is

$$
(JWJ^\top)_{eh}=J_e W J_h^\top.
$$

There are many contact-to-contact blocks, but all of them are constructed
through the same six wrench coordinates. Algebraically,

$$
\operatorname{rank}(JWJ^\top)\le6.
$$

Therefore, the matrix is **diagonal plus a rank-at-most-six correction**.
The full matrix can still have rank $3d$, because $D$ supplies the
remaining directions. Low-rank coupling does not mean that the complete
system is rank deficient.

## 4. Derive the small solve directly

No matrix identity needs to be memorized. Start from

$$
Df+JWJ^\top f=r.
$$

Define a six-dimensional auxiliary vector:

$$
y=WJ^\top f.
$$

The original equation now reads

$$
Df+Jy=r.
$$

Since $D$ is diagonal with positive entries, solving with it is just
componentwise division:

$$
\boxed{f=D^{-1}(r-Jy).}
$$

We do not yet know $y$, but its definition supplies the missing equation.
Substitute the expression for $f$:

$$
\begin{aligned}
y
&=WJ^\top D^{-1}(r-Jy)\\
&=WJ^\top D^{-1}r-WJ^\top D^{-1}Jy.
\end{aligned}
$$

Move the term containing $y$ to the left:

$$
\boxed{
\underbrace{(I_6+WJ^\top D^{-1}J)}_{S\in\mathbb R^{6\times6}}y
=WJ^\top D^{-1}r.
}
$$

The algorithm is now:

1. Assemble and factor $S=I_6+WJ^\top D^{-1}J$.
2. Form $t=WJ^\top D^{-1}r$, a six-component vector.
3. Solve $Sy=t$.
4. Reconstruct every force component with $f=D^{-1}(r-Jy)$.

The reduction is exact in exact arithmetic. Floating-point implementations can
have different rounding errors from a direct solve, so residual/parity checks
still matter.

## 5. How this is the Woodbury identity

Substituting the small-system solution back into the force equation gives

$$
f=
\left[
D^{-1}
-D^{-1}J(I_6+WJ^\top D^{-1}J)^{-1}WJ^\top D^{-1}
\right]r.
$$

Therefore,

$$
\boxed{
(D+JWJ^\top)^{-1}
=D^{-1}
-D^{-1}J(I_6+WJ^\top D^{-1}J)^{-1}WJ^\top D^{-1}.
}
$$

This is the Woodbury identity in a form that does **not** require $W^{-1}$.
It follows from the update formula for $A+UV$, taking
$A=D$, $U=J$, and $V=WJ^\top$.

That detail matters here: some wrench weights may be zero, and a boundary
body uses $W=0$. The reduction remains valid for singular $W$, provided
the systems being solved are invertible. In the boundary case,

$$
S=I_6,\qquad y=0,\qquad f=D^{-1}r.
$$

The inverse notation explains the algebra. The implementation does not build
an explicit inverse of $S$; it factorizes $S$ and solves for $y$.
Only $D^{-1}$ is stored explicitly, as a vector of reciprocal diagonal
entries.

## 6. Why this does not lose individual contact forces

Six wrench coordinates cannot uniquely describe $3d$ force coordinates.
For example, different contact forces can cancel and produce the same net
wrench. How can a six-dimensional solve recover the full answer?

Because $y$ is only the **coupling correction**. Reconstruction also retains
all $3d$ entries of $r$ and $D$:

$$
f_k=\frac{r_k-J_{k,:}y}{D_{kk}},
\qquad k=1,\ldots,3d.
$$

The contact-specific information has not been compressed into $y$.
Each coordinate has its own right-hand side, diagonal penalty, and Jacobian
row.

To see the role of self-balanced forces, consider a vector $z$ satisfying
$J^\top z=0$. Then

$$
JWJ^\top z=0,
\qquad (D+JWJ^\top)z=Dz.
$$

Such force patterns are invisible to the wrench term but still affect the
diagonal terms and the contact constraints enforced by ADMM. They are not
discarded by the reduction.

## 7. A small example you can calculate by hand

Use three scalar force unknowns and one aggregate coordinate to keep the
arithmetic short. This is a rank-one algebra example, not a complete frictional
contact problem.

Let

$$
D=\operatorname{diag}(1,2,4),\qquad
J=\begin{bmatrix}1\\1\\1\end{bmatrix},\qquad
W=[2],\qquad
r=\begin{bmatrix}1\\2\\8\end{bmatrix}.
$$

The direct system would be

$$
\begin{bmatrix}
3&2&2\\
2&4&2\\
2&2&6
\end{bmatrix}f
=
\begin{bmatrix}1\\2\\8\end{bmatrix}.
$$

First perform the diagonal operations:

$$
D^{-1}r=\begin{bmatrix}1\\1\\2\end{bmatrix},
\qquad
J^\top D^{-1}J=1+\frac12+\frac14=\frac74.
$$

The reduced system has just one unknown:

$$
S=1+2\cdot\frac74=\frac92,
\qquad t=2(1+1+2)=8,
\qquad y=\frac{t}{S}=\frac{16}{9}.
$$

Reconstruct the three force components:

$$
f=
\begin{bmatrix}
1-16/9\\
1-(16/9)/2\\
2-(16/9)/4
\end{bmatrix}
=
\boxed{\begin{bmatrix}-7/9\\1/9\\14/9\end{bmatrix}}.
$$

Multiplying this vector by the original 3횞3 matrix gives exactly $r$.
We solved one scalar equation, but still recovered three different unknowns.
The negative entry is allowed in this unconstrained algebra example; actual
contact-cone enforcement belongs to the other ADMM phase.

For a rigid body, the same argument uses up to six aggregate coordinates
instead of one.

## 8. A reproducible 30-variable versus 6-variable example

This NumPy example represents ten contact incidences. It uses a synthetic
Jacobian to isolate the linear algebra; it is not a geometric scene.

```python
import numpy as np

rng = np.random.default_rng(7)
d = 10
J = rng.normal(size=(3 * d, 6))
D_diag = 1.0 + rng.random(3 * d)  # strictly positive
W = np.diag([2.0, 1.0, 3.0, 0.5, 0.0, 0.0])  # singular W is allowed
r = rng.normal(size=3 * d)

# Direct 30 x 30 reference solve.
H = np.diag(D_diag) + J @ W @ J.T
f_direct = np.linalg.solve(H, r)

# Woodbury reduction: diagonal scaling, then a 6 x 6 solve.
D_inv = 1.0 / D_diag
D_inv_J = D_inv[:, None] * J
S = np.eye(6) + W @ (J.T @ D_inv_J)
t = W @ (J.T @ (D_inv * r))
y = np.linalg.solve(S, t)
f_reduced = D_inv * r - D_inv_J @ y

relative_residual = np.linalg.norm(H @ f_reduced - r) / np.linalg.norm(r)
print("Force difference:", np.linalg.norm(f_direct - f_reduced))
print("Relative residual:", relative_residual)
np.testing.assert_allclose(f_reduced, f_direct, rtol=1e-12, atol=1e-12)
assert relative_residual < 1e-12
```

This example uses NumPy's double precision for checking the derivation. The
GPU implementation uses FP32 and has separately declared parity tolerances.

## 9. Why the code uses LU for the reduced matrix

For the usual nonnegative wrench weights, $W$ is symmetric positive
semidefinite. With positive $D$, the original matrix
$D+JWJ^\top$ is symmetric positive definite.

However, define

$$
G=J^\top D^{-1}J.
$$

Although $W$ and $G$ are symmetric, their product generally is not:

$$
(WG)^\top=GW\ne WG.
$$

Thus, the reduced matrix we actually assemble,

$$
S=I_6+WG,
$$

is generally nonsymmetric. Applying Cholesky directly to this $S$ would
be incorrect. The current CPU and GPU implementations use partial-pivot LU.

A symmetric alternative exists if we factor $W=LL^\top$. With $U=JL$,
we could instead use the small symmetric system $I+U^\top D^{-1}U$.
That is a different assembly/reconstruction formula; the current code keeps
the LU form, which also handles zero wrench weights without inverting $W$.

## 10. Locate each operation in stacking-core

The CPU implementation is in
[`ForceGraph::solve_graph_admm`](../src/posegen/force_graph.cpp).
The relevant names map directly to the derivation:

| Derivation | CPU expression/name |
| --- | --- |
| $J$ | `node.jac` |
| $W$ | `k_wrench`, zero for a boundary |
| $D^{-1}$ | `node.d_inv` |
| $D^{-1}J$ | `node.d_inv_jac` |
| $S$ | `capacitance` |
| Factorization of $S$ | `node.capacitance_lu` |
| $r$ | `*node.rhs` after subtracting `node.q` |
| $y$ | `proj` |
| $f$ | `*node.force` |

The key CPU operations are:

```cpp
node.d_inv =
  (node.lhs_diag_base.array() + node.lhs_scale->array()).inverse();
node.d_inv_jac = node.d_inv.asDiagonal() * node.jac;

Matrix6 capacitance = Matrix6::Identity();
capacitance.noalias() +=
  k_wrench * (node.jac.transpose() * node.d_inv_jac);
node.capacitance_lu.compute(capacitance);

*node.rhs -= node.q;
Vector6 const proj = node.capacitance_lu.solve(
  k_wrench * (node.d_inv_jac.transpose() * *node.rhs));
*node.force = node.d_inv.array() * node.rhs->array();
node.force->noalias() -= node.d_inv_jac * proj;
```

The GPU equivalent is the `bodies` kernel in
[`src/posegen/cuda/force.cu`](../src/posegen/cuda/force.cu):

- Assemble $G$ by summing contributions from every incidence.
- Assemble and factor $I_6+WG$ when the job's factorization is dirty.
- Gather the six entries of $J^\top D^{-1}r$.
- Solve for `proj` using the saved LU factors.
- Iterate over all `3 * b.count` force coordinates to reconstruct $f$.

The GPU need not store a separate full $D^{-1}J$ array: it applies each
incidence's reciprocal diagonal while gathering/reconstructing.

Within a frozen graph solve, $J$ and $W$ stay fixed. The factorization
can be reused while $D$ stays fixed too. A beta change changes $D$ and
invalidates that job's factors. A changed right-hand side alone does not.

## 11. What still scales with the contacts on GPU?

Let $n=3d$ and let the small dimension be $k=6$.

| Work or storage | Dense direct approach | Current reduction |
| --- | --- | --- |
| Dense matrix storage | $O(n^2)$ | No dense $n\times n$ matrix |
| Factorization | $O(n^3)$ | $O(k^3)$, after $O(nk^2)$ assembly |
| Solve with cached factors | $O(n^2)$ | $O(nk+k^2)$ |
| Jacobian and force/dual state | Still needed | Still needed, grows with contacts |

These are operation counts, not a guarantee that the reduction is faster for
every small graph. With one contact, for example, the direct system is only
3횞3; the fixed 6횞6 form is useful for its uniform structure and for bodies
with many contacts.

The GPU allocates bounded, padded contact/incidence storage **per job**.
Each body has an `offset` and `count` identifying its incidences. A warp
processes those entries in strides; it does not need a padded dense
$3d_{\max}\times3d_{\max}$ matrix for every body.

Therefore:

- The factorization size is fixed.
- The force vector, dual state, and Jacobian storage are variable in active size.
- Their allocated job capacities are bounded and padded.
- Gathering, reconstruction, cone projection, and residual work grow with contacts.

## 12. Relation to contact-force / velocity duality

In a velocity-based constrained contact formulation, the contact multipliers
or impulses indeed live in contact space. Schematically, with global
quantities and a consistent impulse convention,

$$
v=v_{\mathrm{free}}+M^{-1}J^\top\lambda.
$$

Eliminating velocity gives

$$
u=u_{\mathrm{free}}+JM^{-1}J^\top\lambda,
\qquad u_{\mathrm{free}}=Jv_{\mathrm{free}}.
$$

For $m$ three-component contacts and $N$ free 3D rigid bodies, the stacked
contact variable $\lambda$ has $3m$ entries, while the body velocities
have $6N$. The resulting contact-space operator is $3m\times3m$.
Eliminating one set of variables does not change how many physical contact
variables the problem contains.

The same dimensional structure makes the current body reduction possible:
many contact coordinates interact through a smaller body space. There are,
however, important differences in the present posegen code:

- Posegen's contact forces are the **primal unknowns** of its static force
  optimization problem. Calling contact forces dual variables in a different,
  velocity-based formulation is consistent with this.
- Posegen's $W$ is a wrench-error weight, not an inverse mass matrix.
- The six-dimensional $y=WJ^\top f$ used above is an algebraic auxiliary,
  not the body's simulated velocity.
- The ADMM consensus and cone duals are additional variables associated with
  the chosen splitting; they are not the physical contact force itself.
- Obtaining independent 6횞6 body updates relies on that splitting. Woodbury
  alone does not turn a globally coupled contact problem into independent
  body solves.

Every contact force remains present throughout the algorithm. The reduction
only exploits the structure of the linear algebra used to update those forces.
