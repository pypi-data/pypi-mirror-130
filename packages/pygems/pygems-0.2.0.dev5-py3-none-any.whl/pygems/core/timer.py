import timeit
from typing import Callable

TimeFunc = Callable[[],float]

class Timer:
    """Generic Timer class.

    Parameters
    ----------
    name : `str`
        Name of the timer. Available as :attr:`name` attribute.
    time_func : callback, optional
        Function to be used to retrieve current time (`timeit.default_timer` is used by default). Also 
        available as :attr:`time_func` property.

    stop_func : callback, optional
        Function to be called when the :meth:`stop` method is called. Also available a :attr:`stop_func` property.

    The Timer class is useful for capturing the execution time of long-running operations.

    Examples:

    In this example we will create a timer which prints the elapsed time each time the :meth:`~stop` method is called 
    using a callback function ``stop_func``.

    Another callback function ``time_func`` is used to retrieve the current time.
    

    .. testsetup:: *

       from pygems.core.timer import *
       from functools import partial
       time_func = partial([1, 9.1234, 30.789].pop, 0)
       stop_func = lambda t, *args: print(f'{t.name}:', *args, f'{round(t.elapsed,6)}s')

    .. doctest::

        >>> timer = Timer(name='MyTimer', time_func=time_func, stop_func=stop_func)


    Call the stop() method, passing a stop point name prints the formatted message, passing the stop point name::
        >>> timer.stop('load finished at')
        MyTimer: load finished at 8.1234s

        >>> timer.stop('parse finished at')
        MyTimer: parse finished at 29.789s

    In this example a fake ``time_func`` timer function and custom ``stop_func`` callback are used for illustrative purposes.
    
    ::

       # We use partial to make our fake timer function.
       from functools import partial

       # A fake timer function which will pop and return the first element of a list
       # each time it has been called.
       time_func = partial([1, 9.1234, 30.789].pop, 0)

       # Custom stop_func which prints a formatted message.
       stop_func = lambda t, *args: print(f'{t.name}:', *args, f'{round(t.elapsed,6)}s')

    """
    name: str
    started_at: float
    stopped_at: float
    _time_func: Callable
    _stop_func: Callable

    def __init__(self, name=None, time_func:TimeFunc=None, stop_func=None):
        """Creates, initializes and starts Timer instance.

        name argument is set to name attribute::
            >>> timer = Timer(name='My Timer')
            >>> timer.name
            'My Timer'

        When time_func argument is specified it is set to _time_func attribute::
            >>> time_func = lambda : 20
            >>> timer = Timer(time_func=time_func)
            >>> time_func == timer._time_func
            True

        When time_func argument is not specified, timeit.default_timer is used::
            >>> timer = Timer()
            >>> timer._time_func == timeit.default_timer
            True

        Attempt to use time_func which is not callable raises AssertionError::
            >>> timer = Timer(time_func=5)
            Traceback (most recent call last):
            ...
            AssertionError: Expecting time_func argument to be callable

        Newly created object is started::
            >>> timer = Timer(time_func=[1].pop)
            >>> timer.started_at
            1

        stop_func is set to passed argument::
            >>> timer = Timer(stop_func=print)
            >>> timer.stop_func is print
            True

        Attempt to use stop_func which is not callable raises AssertionError::
            >>> timer = Timer(stop_func=5)
            Traceback (most recent call last):
            ...
            AssertionError: Expecting stop_func argument to be callable

        """
        self.name = name
        if time_func:
            assert callable(time_func), 'Expecting time_func argument to be callable'
        self._time_func = time_func or timeit.default_timer
        if stop_func:
            assert callable(stop_func), 'Expecting stop_func argument to be callable'
        self._stop_func = stop_func
        self.start()

    @property
    def time(self):
        """The current time as returned by the :attr:`time_func` function.
        
        Example:

        >>> timer = Timer(time_func=lambda : 5)
        >>> timer.time
        5
        """
        return self._time_func()

    @property
    def time_func(self) -> TimeFunc:
        """The function used to get the current time."""
        return self._time_func

    @property
    def stop_func(self) -> Callable:
        """Function to be called after at the end of the :meth:`stop` method."""
        return self._stop_func

    @property
    def elapsed(self) -> float:
        """Returns elapsed time between sarted and stopped or started and current time.

        If timer is not stopped, elapsed returns current - started time::
            >>> from functools import partial
            >>> timer = Timer(time_func=partial([1,5].pop, 0))
            >>> timer.elapsed
            4

        If timer is stopped, elapsed returns stopped time - started time::
            >>> timer = Timer(time_func=partial([1,3,5].pop, 0))
            >>> timer.stop()
            >>> timer.stopped_at
            3
            >>> timer.elapsed
            2

        """
        if self.stopped_at:
            return self.stopped_at - self.started_at
        return self.time - self.started_at

    def start(self):
        """Starts the timer by setting the started_at to current time and stopped_at to None.
        
        Example::
            >>> from functools import partial
            >>> timer = Timer(time_func=partial([10,20,30].pop, 0))

        started_at is set during intialization::
            >>> timer.started_at
            10

        When we stop the timer, stopped_at is set::
            >>> timer.stop()
            >>> timer.stopped_at
            20

        Starting a stopped timer sets started_at to current time and stopped_at to None::
            >>> timer.start()
            >>> timer.started_at
            30
            >>> timer.stopped_at is None
            True

        """
        self.started_at = self.time
        self.stopped_at = None

    def stop(self, *args):
        """Stop the timer by setting the stopped_at attribute to current time

        When the :meth:`stop` method is called:
           1. Set the :attr:`stopped_at` attribute to the current time
           2. Determine if :attr:`stop_func` attribute is set to a callback
           3. If the callback is set, call it passing the :class:`Timer` object
              as a first argument, followed by all arguments, received by the :meth:`stop` method. 

        Example::
            >>> from functools import partial
            >>> timer = Timer(time_func=partial([1,9, 50].pop, 0))

        When timer is not stopped, stopped time stopped_at is None::
            >>> timer.stopped_at is None
            True

        After we call the stop() method, the stopped_at time is set to current time::
            >>> timer.stop()
            >>> timer.stopped_at
            9

        Calling stop() method multipe times is safe. Each call remembers current time when stop() was called::
            >>> timer.stop()
            >>> timer.stopped_at
            50

        When stop_func attribute is set, it is called when timer stop() metod is called with timer passed as first artument::
            >>> timer = Timer(name='MyTimer', time_func=partial([1,9.1234,30.789].pop, 0), 
            ...               stop_func=lambda t, *args: print(f'{t.name}:', *args, f'{round(t.elapsed,6)}s'))
            >>> timer.stop('load finished at')
            MyTimer: load finished at 8.1234s
            >>> timer.stop('parse finished at')
            MyTimer: parse finished at 29.789s
        """
        self.stopped_at = self.time
        if hasattr(self, 'stop_func') and self.stop_func:
            # deepcode ignore WrongNumberOfArguments: False negative result
            self.stop_func(self, *args)


class StringMessageCallback:
    """Simple string message callback for the :class:`Timer`'s :meth:`~Timer.stop` method

    Example 1::
        >>> timer = Timer(name='MyTimer', stop_func=StringMessageCallback())
        >>> timer.stop('loaded')          # doctest: +SKIP
        MyTimer: 2.7700000000019376e-05s loaded
        >>> timer.stop('transferred')     # doctest: +SKIP
        MyTimer: 5.060000000001175e-05s transferred

    Example 2: Custom template could be used::
        >>> timer = Timer(name='MyTimer', stop_func=StringMessageCallback(message_template='{args[0]} at {timer.elapsed}s'))
        >>> timer.stop('Loaded')          # doctest: +SKIP
        Loaded at 2.7700000000019376e-05s
        >>> timer.stop('Transfered')      # doctest: +SKIP
        Transfered at 5.060000000001175e-05s
    """
    arg_separator: str = ' '
    """Separator to use when joining the callback arguments before passing to :attr:`message_func`"""

    message_template: str = '{timer.name}: {timer.elapsed}s {args_str}'
    """Template to use to format the output string"""

    message_func: Callable
    """Function to be used to print the output. Default is the `print` function"""

    def __init__(self, message_template=None, message_func=None, arg_separator=None):
        self.message_template = message_template or self.message_template
        self.message_func = message_func or print
        self.arg_separator = arg_separator or self.arg_separator

    def __call__(self, timer, *args):
        """
        >>> from functools import partial
        >>> time_func = partial([1, 10, 30].pop, 0)
        >>> timer = Timer(name='Swiss', time_func=time_func, stop_func=StringMessageCallback())
        >>> timer.stop('load')
        Swiss: 9s load
        """
        message = self.message_template.format(timer=timer, args=args, 
                args_str=self.arg_separator.join(args))
        self.message_func(message)


if __name__ == "__main__": # pragma: no cover
    import doctest
    doctest.testmod()
