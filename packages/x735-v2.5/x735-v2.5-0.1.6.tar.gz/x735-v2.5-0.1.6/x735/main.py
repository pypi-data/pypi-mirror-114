import click
import time
from x735.fan import SetFan, ReedFan, get_cpu_temp, get_fun_speed
from x735.config import fun_speed_range


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def fan(ctx, debug):
    click.echo("Debug mode is {}".format("on" if debug else "off"))
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@fan.command()
@click.pass_context
def run(ctx):
    """Script for running fan"""
    fan = SetFan()
    while True:
        temp = get_cpu_temp()
        if ctx.obj["DEBUG"]:
            click.echo("Temperatura {}".format(temp))

        fun_speed = get_fun_speed(temp, fun_speed_range)
        if ctx.obj["DEBUG"]:
            click.echo("Fun speed {}".format(fun_speed))

        fan.set_speed(fun_speed)
        time.sleep(1)


@fan.command()
@click.pass_context
def info(ctx):
    """Print fan debug info"""
    fan = ReedFan()
    fan.subscribe_turnover()
    while True:
        click.echo("{0:.2f} RPM".format(fan.rpm))
        fan.rpm = 0
        time.sleep(1)
