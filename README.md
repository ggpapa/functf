# functf

This site is for learning various exploitation techniques.
* to learn sellfish/how2heap
* based on shellfish/how2heap

| File | Description | CTF |
|------|-------------|-----|
| fs_arbi_write (1), fs_arbi_read (2) | Play with File Structure (angelboy) ||
| house_of_spiritO (3) | free fake fastbin | hack.lu 2014-OREO (4) |
| bypass_vtable (5) | FILE Structure Exploitation ('vtable' check bypass)	(Dhaval Kapil) | 2017 hctf babyprintf	34c3 300 (6), 2017-babyprintf (7) |
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
