# Dynamic BEAST

This command line tool can be used to create a dynamic version of BEAST 2 XML files. This dynamic XML file can be used to set BEAST parameters at runtime, which can be useful for testing different configurations or quickly modifying parameters without having to edit the XML file. 

To make a BEAST XML file dynamic simple pass it to the tool. 

```
dynamic-beast BEAST.xml
```

This will produce a `dynamic_BEAST.xml` file that can be used as standard in a BEAST analysis.

The `dynamic-beast` tool replaces all the parameter values in the XML file with `$(id.key=value)` format. The value variable is the default value that was initially specified in the XML file. However, the value can be redefined when running a BEAST analysis by making use of the BEAST2 definitions argument (`-D`) that allows for user specified values. 

For example, change the sampling frequency of a sampling:

```bash
beast -D ‘mcmc.ChainLength=100000000,treelog.logEvery=10000,tracelog.logEvery=10000’ dynamic_mcmc.xml
``` 

To ensure reproducibility you should recreate static XML files of runs using dynamic parameters, this can be achieved using the `-DFout` argument e.g., `beast -D ‘clockRate=0.0002’ -DFout static_mcmc.xml dynamic_mcmc.xml`. 