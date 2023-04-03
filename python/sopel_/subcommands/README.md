This is an example showing off user-defined subcommands for the IRC bot [Sopel](https://sopel.chat)

### Sample output

```
<SnoopJ> !dummy
<testibot> base command, invoked as '!dummy'
<SnoopJ> !dummy:subcmd1
<testibot> dummy:subcmd1 subcommand (args=(42,), kwargs={'moredata': 'Twas brillig and the slithy toves'})
<SnoopJ> !dummy:subcmd2
<testibot> dummy:subcmd2 subcommand (args=(42,), kwargs={'moredata': 'Twas brillig and the slithy toves'})
<SnoopJ> !dummy:fakesub
<testibot> base command, invoked as '!dummy:fakesub'
<SnoopJ> !version
<testibot> [version] Sopel v8.0.0.dev0 | Python: 3.7.16 | Commit: b5eba03ce74baae36e3456ac938686fb23f5671b
```
