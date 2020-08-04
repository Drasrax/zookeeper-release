--- ./src/packages/rpm/spec/zookeeper.spec.orig	2012-12-19 18:28:23.668638175 +0100
+++ ./src/packages/rpm/spec/zookeeper.spec	2012-12-19 18:36:17.569429697 +0100
@@ -70,7 +70,7 @@
 Prefix: %{_log_dir}
 Prefix: %{_pid_dir}
 Prefix: %{_var_dir}
-Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service, jdk >= 1.6
+Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service, java >= 1.6
 AutoReqProv: no
 Provides: zookeeper
 
@@ -87,17 +87,14 @@
 ZooKeeper C client library for communicating with ZooKeeper Server.
 
 %prep
-%setup -D -b 1 -n %{_final_name}
-%setup -D -a 0 -n %{_final_name}
+%setup -q -D -b 1 -n %{_final_name}
+%setup -q -D -a 0 -n %{_final_name}
 
 %build
 mkdir -p ${RPM_BUILD_DIR}%{_prefix}
 mkdir -p ${RPM_BUILD_DIR}%{_bin_dir}
 mkdir -p ${RPM_BUILD_DIR}%{_include_dir}
 mkdir -p ${RPM_BUILD_DIR}%{_lib_dir}
-%ifarch amd64 x86_64
-mkdir -p ${RPM_BUILD_DIR}%{_lib64_dir}
-%endif
 mkdir -p ${RPM_BUILD_DIR}%{_libexec_dir}
 mkdir -p ${RPM_BUILD_DIR}%{_log_dir}
 mkdir -p ${RPM_BUILD_DIR}%{_conf_dir}
@@ -118,14 +115,15 @@
 #########################
 %install
 pushd ${RPM_BUILD_DIR}
-mv ${RPM_BUILD_DIR}/%{_final_name}/bin/* ${RPM_BUILD_DIR}%{_bin_dir}
-mv ${RPM_BUILD_DIR}/%{_final_name}/libexec/* ${RPM_BUILD_DIR}%{_libexec_dir}
-mv ${RPM_BUILD_DIR}/%{_final_name}/share/zookeeper/* ${RPM_BUILD_DIR}%{_share_dir}
-mv ${RPM_BUILD_DIR}/%{_final_name}/conf/* ${RPM_BUILD_DIR}%{_conf_dir}
-mv ${RPM_BUILD_DIR}/%{_final_name}/sbin/* ${RPM_BUILD_DIR}%{_sbin_dir}
-cp -f ${RPM_BUILD_DIR}%{_conf_dir}/zoo_sample.cfg ${RPM_BUILD_DIR}%{_conf_dir}/zoo.cfg
+cp -a ${RPM_BUILD_DIR}/%{_final_name}/bin/*.sh ${RPM_BUILD_DIR}%{_bin_dir}
+cp -a ${RPM_BUILD_DIR}/%{_final_name}/libexec/*.sh ${RPM_BUILD_DIR}%{_libexec_dir}
+cp -a ${RPM_BUILD_DIR}/%{_final_name}/share/zookeeper/* ${RPM_BUILD_DIR}%{_share_dir}
+cp -a ${RPM_BUILD_DIR}/%{_final_name}/conf/* ${RPM_BUILD_DIR}%{_conf_dir}
+cp -a ${RPM_BUILD_DIR}/%{_final_name}/sbin/*.sh ${RPM_BUILD_DIR}%{_sbin_dir}
+rm -r ${RPM_BUILD_DIR}/usr/include
+rm -r ${RPM_BUILD_DIR}/usr/man
+mv etc usr var %{buildroot}
 popd ${RPM_BUILD_DIR}
-rm -rf ${RPM_BUILD_DIR}/%{_final_name}
 
 %pre
 getent group hadoop 2>/dev/null >/dev/null || /usr/sbin/groupadd -r hadoop
@@ -153,9 +151,16 @@
 %defattr(-,root,root)
 %attr(0755,root,hadoop) %{_log_dir}
 %attr(0775,root,hadoop) %{_pid_dir}
+%attr(0775,root,hadoop) %{_var_dir}
 %attr(0775,root,hadoop) /etc/init.d/zookeeper
+%dir %{_conf_dir}/
 %config(noreplace) %{_conf_dir}/*
-%{_prefix}
+%{_libexec_dir}/*
+%{_sbin_dir}/*
+%{_share_dir}/*
+%{_log_dir}/
+%{_pid_dir}/
+%{_var_dir}/
 
 %post lib
 /sbin/ldconfig
@@ -163,4 +168,4 @@
 %files lib
 %defattr(-,root,root)
 %{_prefix}/lib/*
-%{_prefix}/bin
+%{_prefix}/bin/*
