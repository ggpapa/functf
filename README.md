# functf (easy)

This site is for learning various easy exploitation techniques.
* to learn sellfish/how2heap
* based on shellfish/how2heap

| File | Description | CTF |
|------|-------------|-----|
| fs_arbi_write (1), fs_arbi_read (2) | Play with File Structure (angelboy) ||
| house_of_spiritO (3) | free fake fastbin | hack.lu 2014-OREO (4) |
| bypass_vtable (5) fs_arbi_w_babe (6) | FILE Structure Exploitation ('vtable' check bypass)	(Dhaval Kapil) | 2017-babyprintf (7) |
| unsorted_binO	(8) | change arbitrary address as arena value | 0ctf 2016-zerostorage (9) |
| fastbin_dup_into_stackO (10) | abusing the fastbin freelist.	| 9447-search-engine (11), 0ctf 2017-babyheap (12) |
| unsafe_unlinkO (13) |	free on a corrupted chunk to get arbitrary write. |HITCON CTF 2014-stkof (14), Insomni'hack 2017-Wheel of Robots (15) |
| poison_null_byteO (16) |	a single null byte overflow. | PlaidCTF 2015-plaiddb (17) |
| house_of_loreO (18) | abusing the smallbin freelist.	||
| overlapping_chunksO (19)	| the overwrite of a freed chunk size in the unsorted bin | hack.lu CTF 2015-bookstore (20), Nuit du Hack 2016-night-deamonic-heap (21) |
| overlapping_chunks_2_O (22) | the overwrite of an in use chunk size||
| house_of_forceO (23) |	the Top Chunk (Wilderness) header | Boston Key Party 2016-cookbook (24), BCTF 2016-bcloud (25) |
| house_of_einherjarO (26) | a single null byte overflow | Seccon 2016-tinypad (27) |
| house_of_orangeO (28)	| the Top Chunk (Wilderness) | Hitcon 2016 houseoforange (29), 34C3 300 (30) |
| tcache_house_of_spiritO (31)	| same with house_of_spirit ||

# functf (babe)

This site is for learning various babe exploitation techniques.
* ref 1. shellfish/how2heap
* ref 2. BOF Won Jung Dae
* ref 3. protos/nebulas

| File | Description |
|------|-------------|
| problem_child | you need a little bit bruth force (1~255 times). nc functf 18001 |
| remote_32_first	| 17.10 call stack is different from 16.04. NO need to leak, nc functf 18002 |
| remote_32_babe | if you pass the first step, just add some leaks. Need to leak, NO BF! nc functf 18003	|
| remote_64_next | In 64bit, functions use register for args. use good gadgets nc functf 18004	|
| remote_64_babe | Leak libc address with rop gadgets. nc functf 18005|
| stack_easy | stack is always easy one. nc functf 18006	exp_stack_easy
| start_fms	| FMS bug can read stack value. nc functf 18007|
| bss_fms | FMS bug can change BSS value. nc functf 18008|
| bss_fms2 | Cause of compiler, task becomes harder but you can do it. had to patch it. could not use DTORS, used GOT. nc functf 18009|
| bss_fms_easy | one of the easist format string bug. nc functf 18010|
| start_heap | Heap starts. nc functf 18011|
| twin_heap |	Full Relo and Partial Relo are different. nc functf 18012|
| login_heap | Is it funny? I think it's funny. nc functf 18013|
| triple_heap | Let's start a easy fastbin. nc functf 18014|
| start_nw |	Time base random. It is vulnerable. CDLL is helpful.(Asia/Seoul) nc functf 18015	|
| test_your_name |	gets() cannot read the following '\n'(0x0a) characters. nc functf 18016	|
| test_blind_fms |	blind is not a real blind.nc functf 18017	|
| test_heap | unsafed unlink(16.04, 17.10).nc functf 18018	|
| ad_stack |	ref. realpath() bug, socat and xinet.d, their stack is different. It need a little BF. nc functf 18019	|
| ad_stack_babe |	realpath() bug 2. You CAN use ad_stack exploit. Don't u? nc functf 18020	|
| ad_stack_cript | usual stack overflow.nc functf 18021	|
| triple_heap_babe | twin heap -> use fast bins. nc functf 18022	|
