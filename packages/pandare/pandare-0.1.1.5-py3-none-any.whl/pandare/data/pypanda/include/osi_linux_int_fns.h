
// returns fd for a filename or a NULL if failed
char *osi_linux_fd_to_filename(CPUState *env, OsiProc *p, int fd);

// returns pos in a file 
unsigned long long osi_linux_fd_to_pos(CPUState *env, OsiProc *p, int fd);

target_ptr_t ext_get_file_struct_ptr(CPUState *env, target_ptr_t task_struct, int fd);
target_ptr_t ext_get_file_dentry(CPUState *env, target_ptr_t file_struct);
