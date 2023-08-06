sf-apm-lib
==============

Snappyflow modules

Installation
------------
pip install sf-apm-lib

Usage
-----
* Get trace config

    ```    
    from sf_apm_lib import snappyflow as sf
    trace_config = sf.get_trace_config(<Snappyflow Profile Key>, <Project Name>, <App Name>)
    ```
