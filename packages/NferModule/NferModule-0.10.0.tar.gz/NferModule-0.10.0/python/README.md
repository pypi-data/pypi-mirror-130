Nfer for Python - Debugging Asynchronous Programs Made Easier
=============================================================================

To install nfer for Python, use pip:
```Shell
pip install NferModule
```

For nfer to work, either events or intervals must be logged.  There are three ways to do this in Python:
1. Instrumenting function execution
2. Logging other events
3. Generating new intervals with rules

Those events and intervals can then be monitored.  Monitor output takes two forms:
1. Executing Python in response to a rule matching
2. Visualizing in the web-based GUI

## 1. Instrumenting Function Execution
To instrument function execution, you can use the nfer.instrument package.  Instrumented functions are automatically monitored.
```Python
from nfer.instrument import instrument, watch

# to instrument the current execution context
instrument()
# to instrument a specific module or package
instrument('my_module')

# alternatively, you can instrument specific functions manually using the watch annotation
@watch
def my_instrumented_func():
    # watch also works on methods
    pass
```

## Logging Other Events
You can also manually log events which might mark something interesting happening.
```Python
from nfer.nfer import report_event

report_event('myevent')

# events can also carry data, which is passed as a dict
# dict members can only be literals, not lists or other dicts
report_event('myevent', {'id':42, 'debug':False})
```

## Generating New Intervals with Rules
The Python nfer API follows fairly closely with the C language DSL.  [The Docs for that DSL](https://bitbucket.org/seanmk/nfer/src/master/doc/nfer.md) explain the operators and data expressions, so this guide will focus on the specifics of the Python DSL.

Nfer rules are declarative and are triggered when a condition is met.  That condition is always either that one or two other events or intervals are logged where some conditions are met.

Once you create a rule, you need to tell nfer to monitor it.
```Python
from nfer.rules import when
from nfer.nfer import monitor

# wait for myevent to occur
rule = when('myevent')
# give that a new name (the default is a random UUID)
rule.name('new_name')
monitor(rule)

# wait for two events or intervals where the first ends before the second begins
rule2 = when('first').before('second').name('matched')
monitor(rule2)

# events and intervals can have data, and you can filter on these also
# you can add shorthand names by prepending them with a colon
rule3 = when('myevent').during('f:my_instrumented_func')
        .where('myevent.id = f.id').name('ids_match')

# you can create new data items on a generated interval with the map method
rule3.map('matched_id', 'f.id')
# don't forget to monitor it!
monitor(rule3)
```

## Executing Python in Response to a Rule Matching

You can add an optional parameter to the monitor function to have a Python function called when the rule matches.

```Python
from nfer.rules import when
from nfer.nfer import monitor

new_rule = when('func1').slice('func2')
monitor(new_rule, 
  lambda i: print('Funcs 1 and 2 overlapped from %d to %d!' % (i.begin, i.end)))
```

## Visualizing in the Web-Based GUI

You can visualize any monitored rule or interval (instrumented functions are automatically monitored) using a built-in web-based GUI.

```Python
from nfer.gui import gui

# gui arguments:
# 1. the required argument is the intervals to display when the GUI loads, 
#    but this can be changed in the interface
# 2. what data to display on mouseover (by default, function args)
# 3. on which port to run (by default, 5000)
# 4. by default, the GUI function blocks until a client connects
# 5. by default, the GUI opens a web browser pointed at the GUI
gui(intervals=['matched', 'ids_matched'], tooltips=['matched_ids'])
```