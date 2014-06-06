#modpeg

This is a modelica compiler written using the parsimonious PEG parser.

https://github.com/erikrose/parsimonious

##Roadmap

### DONE

* basic parser that can handle helloworld example

### TODO

#### backend representation

We need to create a backend representation of the models that can generate the equations for simulation/ inverse simulation/ jacobians etc.

#### modelica magic

If you have ever used fortran magic I would imagine that modelica magic would work the same way. You would do something like

    %modelica
    model ball
      Real a;
    equation
      der(a) = a;
    end model ball

in one cell, then you get the python object out to play with

    results = ball.simulate(tf=10)
    plot(results.a)

#### real-time simulation

    sim = ode(ball.dynamics)
    while sim.successfull
        sim.integrate(sim.t + dt)
        do real-time stuff
        // wait on wall clock


#### analytical jacobians

for sympy

ball_trimmed = ball.trim(a=1).
A = sympy.jacobian([ball_trimmed.der(a)],[ball_trimmed.a])

#### inverse dynamics
sim = ode(ball.inverse_dynamics)
while sim.successfull
    sim.integrate(sim.t + dt)

vim:ts=4:sw=4:expandtab
