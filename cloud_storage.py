"""
code signal, cloud storage
Level 1
The cloud storage system should support file manipulation.
• ADD_FILE <name> ‹size> — should add a new file name to the storage. size is the amount of memory required in bytes.
The current operation fails if a file with the same name already exists. Returns "true" if the file was added
successfully or "false" otherwise.
• GET_FILE_SIZE <name> - Should return a string representing the size of the file name if it exists, or an empty
string otherwise.
• DELETE_FILE ‹name> — should delete the file name. Returns a string representing the deleted file size if the
deletion was successful or an empty string if the file does not exist.
Level 2
Implement an operation for retrieving some statistics about files with a specific prefix.
• GET_N LARGEST ‹prefix› <n> — should return the string representing the names of the top n-largest files with
names starting with prefix in the following format: "‹name1›(<size1>), ..., <nameN> (<sizeN>)". Returned files
should be sorted by size in descending order, or in case of a tie, sorted in lexicographical order of the names.
If there are no such files, return an empty string. If the number of such files is less than n, all of them
  should be returned in the specified format.
Level 3
Implement support for queries from different users. All users share a common filesystem in the cloud storage system,
 but each user is assigned a storage capacity limit.
• ADD_USER ‹userId ‹capacity› — should add a new user in the system, with capacity as their storage limit in bytes.
 The total size of all files owned by userId cannot exceed capacity. The operation fails if a user with userId
 already exists. Returns "true" if a user with userId is successfully created, or "False" otherwise.
• ADD_FILE_BY <userId ‹name> ‹size> - should behave in the same way as the ADD_FILE from Level 1, but the added
 file should be owned by the user with userId. A new file cannot be added to the storage if doing so will exceed
  the user's capacity limit. Returns a string representing the remaining capacity of the user if the file is added
successfully, or an empty string otherwise.
Note that all queries calling the ADD_FILE operation implemented during Level 1 are run by the user with
userId = "admin", who has unlimited storage capacity.
• MERGE_USER <userId1> <userId2> - should merge the account of userId2 with the userId1. Ownership of
 all of userId2 's files is transferred to userId1, and any remaining storage capacity is also added to
 userId1's limit. userId2 is deleted if the merge is successful. Returns a string representing the remaining
  capacity of userId1 after merging, or an empty string if one of the users does not exist or userId1 is
  equal to userId2. It is guaranteed that neither userId1 nor userId2 equals "admin".

Level 4
Implement support to allow users to back up their files.
• BACKUP_USER < userId> - should back up the current state of all files owned by userid - i.e., file names and sizes.
 The backup is stored on a separate storage system and is not affected by any new file manipulation queries.
  Overwrites any backups for the same user if previous backups exist. Returns a string representing the number
  of backed-up files, or an empty string if userid does not exist.
• RESTORE _USER ‹userId> — should restore the state of userId 's files to the latest backup. If there was no backup,
 all of userid 's files are deleted. If a file can't be restored because another user added another file with
  the same name, it is ignored. Returns a string representing the number of the files that are successfully restored
  or an empty string if userId does not exist.

Note that MERGE_USER does not affect userId's backup, and userid2 is deleted along with its backup.
Note that the RESTORE_USER operation does not affect the user's capacity. Badly worded, test cases show capacity
increased back when restore deleted all user's files. It actually means the initial capacity not changed.
"""
