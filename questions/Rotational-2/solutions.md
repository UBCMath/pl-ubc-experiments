# Cans of Pineapples

Two cans of pineapples,
one empty and one unopened,
sit beside each other on a table next to a slope.
James knocks them both over,
and the two cans roll down the slope at the same time.

Which can reaches the bottom of the slope first?

If the cans roll a distance of $d$,
and the slope forms an angle of $\theta$ with the ground,
find the speed of both cans the moment they reach the bottom of the slope,
assuming no work is done by friction.

## Reaching the Bottom

We can approximate the unopened can as a solid cylinder,
and the empty one as a hollow one.

We know **the solid cylinder will reach the bottom first**,
since a solid cylinder has less mass distributed around the rim
and more mass distributed towards the centre,
and thus has a smaller moment of inertia,
which leads to a lower rotational kinetic energy,
higher translational kinetic energy,
and therefore, higher speed.

## How High Are You?

As we are not given any height,
we need to first find that.

$\sin \theta = \frac{h}{d}$

$h = d \sin \theta$

## I Am Speed

As we know there is no energy lost to friction,
we can use conservation of energy to calculate everything.

$E_0 = E_1$

Setting the bottom of the slope as 0 energy:

$U = K_T + K_R$

$mgh = \frac{1}{2}mv^2 + \frac{1}{2}I\omega^2$

## A Solid Run

The moment of inertia for a solid cylinder is
$I = \frac{1}{2}mr^2$.

$mgh = \frac{1}{2}mv^2 + \frac{1}{2}\frac{1}{2}mr^2\omega^2$

By definition of rotational speed $v = r\omega$:

$mgh = \frac{1}{2}mv^2 + \frac{1}{4}mv^2$

$gh = \frac{3}{4}v^2$

$v = \sqrt{\frac{4}{3}gh}$

$v = \sqrt{\frac{4}{3}gd \sin \theta}$

## Getting Beaten Hollow

The moment of inertia for a hollow cylinder is
$I = mr^2$

$mgh = \frac{1}{2}mv^2 + \frac{1}{2}0mr^2\omega^2$

$gh = v^2$

$v = \sqrt{gh}$

$v = \sqrt{gd \sin \theta}$
