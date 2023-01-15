#= 
Author(s): Matteo Manzi, Mattia Petrini
=#

using DifferentialEquations
using LinearAlgebra
using Plots; gr()
using PlotlyJS
using RecipesBase


#σ = 10
ρ = 28
β = 8/3

function Lorenz!(dw,w,σ,t)
    x = w[1]
    y = w[2]
    z = w[3]

    dw_dw0 = [w[4] w[5] w[6]; w[7] w[8] w[9]; w[10] w[11] w[12]]

    dw[1] = σ * y - σ * x
    dw[2] = ρ * x - x * z - y
    dw[3] = x * y - β * z

    dg_dz_11 = -σ
    dg_dz_12 = σ
    dg_dz_13 = 0

    dg_dz_21 = ρ - z
    dg_dz_22 = -1
    dg_dz_23 = -x
    
    dg_dz_31 = y
    dg_dz_32 = x
    dg_dz_33 = -β

    dg_dz = [dg_dz_11 dg_dz_12 dg_dz_13; dg_dz_21 dg_dz_22 dg_dz_23; dg_dz_31 dg_dz_32 dg_dz_33]

    ddt_dw_dw0 = dg_dz * dw_dw0

    dw[4] = ddt_dw_dw0[1, 1]
    dw[5] = ddt_dw_dw0[1, 2]
    dw[6] = ddt_dw_dw0[1, 3]
    dw[7] = ddt_dw_dw0[2, 1]
    dw[8] = ddt_dw_dw0[2, 2]
    dw[9] = ddt_dw_dw0[2, 3]
    dw[10] = ddt_dw_dw0[3, 1]
    dw[11] = ddt_dw_dw0[3, 2]
    dw[12] = ddt_dw_dw0[3, 3]
end

T = 3
t_span = (0.0, T) 

len = 250

FTLE = zeros((len, len))

x0_list = range(-20, 20, length=len)
#x0_list = range(-9, -8, length=len)
y0_list = range(-30, 30, length=len)
#y0_list = range(-16, -15, length=len)
z0 = 20.533978

function my_f(σ)

    i = 0
    for x_0 in x0_list
        println(i)

        i = i + 1
        j = 0
        for y_0 in y0_list
            j = j + 1
            local w_0 = [x_0, y_0, z0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
            local prob = ODEProblem(Lorenz!,w_0,t_span,σ)
            local sol = solve(prob,reltol=1e-2, abstol=1e-2)
            dzt_dz0_array = last(sol)[4:12]
            dzt_dz0 = [dzt_dz0_array[1] dzt_dz0_array[2] dzt_dz0_array[3]; dzt_dz0_array[4] dzt_dz0_array[5] dzt_dz0_array[6]; dzt_dz0_array[7] dzt_dz0_array[8] dzt_dz0_array[9]]
            M1 = [1 0 0; 0 1 0]
            M2 = [1 0; 0 1; 0 0]
            Jacob = M1 * dzt_dz0 * M2
            Delta = transpose(Jacob)*Jacob
            eig_val = eigen(Delta).values
            FTLE_ij = 1/T * log(sqrt(maximum(eig_val)))
            FTLE[i, j] = FTLE_ij 
        end
    end
    return FTLE
end

n = 100
gif_range = range(0, stop = 5, length = n)

anim = @animate for l in gif_range
    println(l)

    f = my_f(l)

    Plots.heatmap(x0_list, y0_list, transpose(f), legend=false, axis=([]))
end 
``
gif(anim, "lorenz_chaos.gif", fps = n/5)
