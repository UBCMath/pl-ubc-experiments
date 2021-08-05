# Rolling and Slipping

A ball with mass $M$ and radius $R$ is slipping on a table
with an initial speed of $v_0$ and no rotational velocity.
Find the time needed to for the ball to go from slipping to rolling,
if the coefficient of friction between the ball and the table is $\mu$ .

## Translational motion

The translational velocity of the ball can be calculated using forces.

$F_{net} = ma$

The force of friction applies opposite to the direction of the ball.

$-F_F = Ma$

$-\mu F_N = Ma$

$-\mu Mg = Ma$

$a = -\mu g$

Since acceleration is constant, the velocity as a function of time is:

$v = v_0 + at$

$v = v_0 - \mu gt$

## Rotational motion

The angular velocity of the ball can be calculated using torques.

$\tau_{net} = I \alpha$

The force of friction applies in the direction of the rotation, at the surface of the ball.

The moment of inertia of a sphere is $\frac{2}{5}MR^2$ .

$RF_F = \frac{2}{5}MR^2 \alpha$

$\mu Mg = \frac{2}{5}MR \alpha$

$\alpha = \frac{5 \mu g}{2R}$

Since angular acceleration is constant, the angular velocity as a function of time is:

$\omega = \omega_0 + \alpha t$

There is no initial angular velocity.

$\omega = \frac{5 \mu g}{2R} t$

## Slip into roll

When a ball is rolling, translational motion is equal to its rotational counterpart.

$v = r \omega$

Substitute in the two expressions we calculated above.

$v_0 - \mu gt = R \frac{5 \mu g}{2R} t$

$v_0 = \mu gt + R \frac{5 \mu g}{2R} t$

$v_0 = \mu gt + \frac{5}{2} \mu gt$

Factor out $\mu gt$ on the right side:

$v_0 = \mu gt (1 + \frac{5}{2})$

$v_0 = \frac{7}{2} \mu gt$

Isolating for $t$ :

$t = \frac{2v_0}{7 \mu g}$
