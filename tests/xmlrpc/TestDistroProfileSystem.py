import os
from xmlrpc.CobblerXmlRpcBaseTest import CobblerXmlRpcBaseTest

FAKE_INITRD = "initrd1.img"
FAKE_INITRD2 = "initrd2.img"
FAKE_INITRD3 = "initrd3.img"
FAKE_KERNEL = "vmlinuz1"
FAKE_KERNEL2 = "vmlinuz2"
FAKE_KERNEL3 = "vmlinuz3"
TEST_POWER_MANAGEMENT = True
TEST_SYSTEM = ""
cleanup_dirs = []


def tprint(call_name):
    """
    Print a remote call debug message

    @param call_name str remote call name
    """

    print("test remote call: %s()" % call_name)


class TestDistroProfileSystem(CobblerXmlRpcBaseTest):
    """
    Test remote calls related to distros, profiles and systems
    These item types are tested together because they have inter-dependencies
    """

    def setUp(self):

        super(TestDistroProfileSystem, self).setUp()

        # Create temp dir
        self.topdir = "/tmp/cobbler_test"
        try:
            os.makedirs(self.topdir)
        except:
            pass

        # create temp files
        self.fk_initrd = os.path.join(self.topdir, FAKE_INITRD)
        self.fk_initrd2 = os.path.join(self.topdir, FAKE_INITRD2)
        self.fk_initrd3 = os.path.join(self.topdir, FAKE_INITRD3)
        self.fk_kernel = os.path.join(self.topdir, FAKE_KERNEL)
        self.fk_kernel2 = os.path.join(self.topdir, FAKE_KERNEL2)
        self.fk_kernel3 = os.path.join(self.topdir, FAKE_KERNEL3)
        self.redhat_kickstart = os.path.join(self.topdir, "test.ks")
        self.suse_autoyast = os.path.join(self.topdir, "test.xml")
        self.ubuntu_preseed = os.path.join(self.topdir, "test.seed")
        self.files_create = [
            self.fk_initrd, self.fk_initrd2, self.fk_initrd3,
            self.fk_kernel, self.fk_kernel2, self.fk_kernel3,
            self.redhat_kickstart, self.suse_autoyast, self.ubuntu_preseed
        ]
        for fn in self.files_create:
            f = open(fn, "w+")
            f.close()

        self.distro_fields = [
            # field format: field_name, good value(s), bad value(s)
            # field order is the order in which they will be set
            # TODO: include fields with dependencies: fetchable files, boot files, etc.
            ["arch", ["i386", "x86_64", "ppc", "ppc64"], ["badarch"]],
            # generic must be last breed to be set so os_version test below will work
            ["breed", ["debian", "freebsd", "redhat", "suse", "ubuntu", "unix", "vmware", "windows", "xen", "generic"],
             ["badbreed"]],
            ["comment", ["test comment", ], []],
            ["initrd", [self.fk_initrd, ], ["", ]],
            ["name", ["testdistro0"], []],
            ["kernel", [self.fk_kernel, ], ["", ]],
            ["kernel_options", ["a=1 b=2 c=3 c=4 c=5 d e", ], []],
            ["kernel_options_post", ["a=1 b=2 c=3 c=4 c=5 d e", ], []],
            ["ks_meta", ["a=1 b=2 c=3 c=4 c=5 d e", ], []],
            ["mgmt_classes", ["one two three", ], []],
            ["os_version", ["generic26", ], ["bados", ]],
            ["owners", ["user1 user2 user3", ], []],
        ]

        self.profile_fields = [
            # field format: field_name, good value(s), bad value(s)
            # TODO: include fields with dependencies: fetchable files, boot files,
            #         template files, repos
            ["comment", ["test comment"], []],
            ["dhcp_tag", ["", "foo"], []],
            ["distro", ["testdistro0"], ["baddistro", ]],
            ["enable_gpxe", ["yes", "YES", "1", "0", "no"], []],
            ["enable_menu", ["yes", "YES", "1", "0", "no"], []],
            ["kernel_options", ["a=1 b=2 c=3 c=4 c=5 d e"], []],
            ["kernel_options_post", ["a=1 b=2 c=3 c=4 c=5 d e"], []],
            ["kickstart", [self.redhat_kickstart, self.suse_autoyast, self.ubuntu_preseed],
             ["/path/to/bad/kickstart", ]],
            ["ks_meta", ["a=1 b=2 c=3 c=4 c=5 d e", ], []],
            ["mgmt_classes", ["one two three", ], []],
            ["mgmt_parameters", ["<<inherit>>"], ["badyaml"]],  # needs more test cases that are valid yaml
            ["name", ["testprofile0"], []],
            ["name_servers", ["1.1.1.1 1.1.1.2 1.1.1.3"], []],
            ["name_servers_search", ["example.com foo.bar.com"], []],
            ["owners", ["user1 user2 user3"], []],
            ["proxy", ["testproxy"], []],
            ["server", ["1.1.1.1"], []],
            ["virt_auto_boot", ["1", "0"], ["yes", "no"]],
            ["virt_bridge", ["<<inherit>>", "br0", "virbr0", "xenbr0"], []],
            ["virt_cpus", ["<<inherit>>", "1", "2"], ["a"]],
            ["virt_disk_driver", ["<<inherit>>", "raw", "qcow2", "vmdk"], []],
            ["virt_file_size", ["<<inherit>>", "5", "10"], ["a"]],
            ["virt_path", ["<<inherit>>", "/path/to/test", ], []],
            ["virt_ram", ["<<inherit>>", "256", "1024"], ["a", ]],
            ["virt_type", ["<<inherit>>", "xenpv", "xenfv", "qemu", "kvm", "vmware", "openvz"], ["bad", ]],
        ]

        self.system_fields = [
            # field format: field_name, good value(s), bad value(s)
            # TODO: include fields with dependencies: fetchable files, boot files,
            #         template files, images
            ["comment", ["test comment"], []],
            ["enable_gpxe", ["yes", "YES", "1", "0", "no"], []],
            ["kernel_options", ["a=1 b=2 c=3 c=4 c=5 d e"], []],
            ["kernel_options_post", ["a=1 b=2 c=3 c=4 c=5 d e"], []],
            ["kickstart", [self.redhat_kickstart, self.suse_autoyast, self.ubuntu_preseed],
             ["/path/to/bad/kickstart", ]],
            ["ks_meta", ["a=1 b=2 c=3 c=4 c=5 d e", ], []],
            ["mgmt_classes", ["one two three", ], []],
            ["mgmt_parameters", ["<<inherit>>"], ["badyaml"]],  # needs more test cases that are valid yaml
            ["name", ["testsystem0"], []],
            ["netboot_enabled", ["yes", "YES", "1", "0", "no"], []],
            ["owners", ["user1 user2 user3"], []],
            ["profile", ["testprofile0"], ["badprofile", ]],
            ["repos_enabled", [], []],
            ["status", ["development", "testing", "acceptance", "production"], []],
            ["proxy", ["testproxy"], []],
            ["server", ["1.1.1.1"], []],
            ["virt_auto_boot", ["1", "0"], ["yes", "no"]],
            ["virt_cpus", ["<<inherit>>", "1", "2"], ["a"]],
            ["virt_file_size", ["<<inherit>>", "5", "10"], ["a"]],
            ["virt_disk_driver", ["<<inherit>>", "raw", "qcow2", "vmdk"], []],
            ["virt_ram", ["<<inherit>>", "256", "1024"], ["a", ]],
            ["virt_type", ["<<inherit>>", "xenpv", "xenfv", "qemu", "kvm", "vmware", "openvz"], ["bad", ]],
            ["virt_path", ["<<inherit>>", "/path/to/test", ], []],
            ["virt_pxe_boot", ["1", "0"], []],

            # network
            ["gateway", [], []],
            ["hostname", ["test"], []],
            ["ipv6_autoconfiguration", [], []],
            ["ipv6_default_device", [], []],
            ["name_servers", ["9.1.1.3"], []],
            ["name_servers_search", [], []],

            # network - network interface specific
            # TODO: test these fields
            ["bonding_opts-eth0", [], []],
            ["bridge_opts-eth0", [], []],
            ["cnames-eth0", [], []],
            ["dhcp_tag-eth0", [], []],
            ["dns_name-eth0", [], []],
            ["if_gateway-eth0", [], []],
            ["interface_type-eth0", [], []],
            ["interface_master-eth0", [], []],
            ["ip_address-eth0", [], []],
            ["ipv6_address-eth0", [], []],
            ["ipv6_secondaries-eth0", [], []],
            ["ipv6_mtu-eth0", [], []],
            ["ipv6_static_routes-eth0", [], []],
            ["ipv6_default_gateway-eth0", [], []],
            ["mac_address-eth0", [], []],
            ["mtu-eth0", [], []],
            ["management-eth0", [], []],
            ["netmask-eth0", [], []],
            ["static-eth0", [], []],
            ["static_routes-eth0", [], []],
            ["virt_bridge-eth0", [], []],

            # power management
            ["power_type", ["lpar"], ["bla"]],
            ["power_address", ["127.0.0.1"], []],
            ["power_id", ["pmachine:lpar1"], []],
            ["power_pass", ["pass"], []],
            ["power_user", ["user"], []]

        ]

    def tearDown(self):

        super(TestDistroProfileSystem, self).tearDown()

        for fn in self.files_create:
            os.remove(fn)

    def _get_distros(self):
        """
        Test: get distros
        """

        tprint("get_distros")
        self.remote.get_distros(self.token)

    def _get_profiles(self):
        """
        Test: get profiles
        """

        tprint("get_profiles")
        self.remote.get_profiles(self.token)

    def _get_systems(self):
        """
        Test: get systems
        """

        tprint("get_systems")
        self.remote.get_systems(self.token)

    def _create_distro(self):
        """
        Test: create/edit a distro
        """

        distros = self.remote.get_distros(self.token)

        tprint("new_distro")
        distro = self.remote.new_distro(self.token)

        tprint("modify_distro")
        for field in self.distro_fields:
            (fname, fgood, fbad) = field
            for fb in fbad:
                try:
                    self.remote.modify_distro(distro, fname, fb, self.token)
                except:
                    pass
                else:
                    self.fail("bad field (%s=%s) did not raise an exception" % (fname, fb))
            for fg in fgood:
                try:
                    result = self.remote.modify_distro(distro, fname, fg, self.token)
                    self.assertTrue(result)
                except Exception as e:
                    self.fail("good field (%s=%s) raised exception: %s" % (fname, fg, str(e)))

        tprint("save_distro")
        self.assertTrue(self.remote.save_distro(distro, self.token))

        # FIXME: if field in item_<type>.FIELDS defines possible values,
        # test all of them. This is valid for all item types
        # for field in item_system.FIELDS:
        #    (fname,def1,def2,display,editable,tooltip,values,type) = field
        #    if fname not in ["name","distro","parent"] and editable:
        #        if values and isinstance(values,list):
        #            fvalue = random.choice(values)
        #        else:
        #             fvalue = "testing_" + fname
        #        self.assertTrue(self.remote.modify_profile(subprofile,fname,fvalue,self.token))

        new_distros = self.remote.get_distros(self.token)
        self.assertTrue(len(new_distros) == len(distros) + 1)

    def _create_profile(self):
        """
        Test: create/edit a profile object"""

        profiles = self.remote.get_profiles(self.token)

        tprint("new_profile")
        profile = self.remote.new_profile(self.token)

        tprint("modify_profile")
        for field in self.profile_fields:
            (fname, fgood, fbad) = field
            for fb in fbad:
                try:
                    self.remote.modify_profile(profile, fname, fb, self.token)
                except:
                    pass
                else:
                    self.fail("bad field (%s=%s) did not raise an exception" % (fname, fb))
            for fg in fgood:
                try:
                    self.assertTrue(self.remote.modify_profile(profile, fname, fg, self.token))
                except Exception as e:
                    self.fail("good field (%s=%s) raised exception: %s" % (fname, fg, str(e)))

        tprint("save_profile")
        self.assertTrue(self.remote.save_profile(profile, self.token))

        new_profiles = self.remote.get_profiles(self.token)
        self.assertTrue(len(new_profiles) == len(profiles) + 1)

    def _create_subprofile(self):
        """
        Test: create/edit a subprofile object"""

        profiles = self.remote.get_profiles(self.token)

        tprint("new_subprofile")
        subprofile = self.remote.new_subprofile(self.token)

        tprint("modify_profile")
        self.assertTrue(self.remote.modify_profile(subprofile, "name", "testsubprofile0", self.token))
        self.assertTrue(self.remote.modify_profile(subprofile, "parent", "testprofile0", self.token))

        tprint("save_profile")
        self.assertTrue(self.remote.save_profile(subprofile, self.token))

        new_profiles = self.remote.get_profiles(self.token)
        self.assertTrue(len(new_profiles) == len(profiles) + 1)

    def _create_system(self):
        """
        Test: create/edit a system object
        """

        systems = self.remote.get_systems(self.token)

        tprint("new_system")
        system = self.remote.new_system(self.token)

        tprint("modify_system")
        self.assertTrue(self.remote.modify_system(system, "name", "testsystem0", self.token))
        self.assertTrue(self.remote.modify_system(system, "profile", "testprofile0", self.token))
        for field in self.system_fields:
            (fname, fgood, fbad) = field
            for fb in fbad:
                try:
                    self.remote.modify_system(system, fname, fb, self.token)
                except:
                    pass
                else:
                    self.fail("bad field (%s=%s) did not raise an exception" % (fname, fb))
            for fg in fgood:
                try:
                    self.assertTrue(self.remote.modify_system(system, fname, fg, self.token))
                except Exception as e:
                    self.fail("good field (%s=%s) raised exception: %s" % (fname, fg, str(e)))

        tprint("save_system")
        self.assertTrue(self.remote.save_system(system, self.token))

        new_systems = self.remote.get_systems(self.token)
        self.assertTrue(len(new_systems) == len(systems) + 1)

    def _get_distro(self):
        """
        Test: get a distro object"""

        tprint("get_distro")
        distro = self.remote.get_distro("testdistro0")

    def _get_profile(self):
        """
        Test: get a profile object"""

        tprint("get_profile")
        profile = self.remote.get_profile("testprofile0")

    def _get_system(self):
        """
        Test: get a system object"""

        tprint("get_system")
        system = self.remote.get_system("testsystem0")

    def _find_distro(self):
        """
        Test: find a distro object
        """

        tprint("find_distro")
        result = self.remote.find_distro({"name": "testdistro0"}, self.token)
        self.assertTrue(result)

    def _find_profile(self):
        """
        Test: find a profile object
        """

        tprint("find_profile")
        result = self.remote.find_profile({"name": "testprofile0"}, self.token)
        self.assertTrue(result)

    def _find_system(self):
        """
        Test: find a system object
        """

        tprint("find_system")
        result = self.remote.find_system({"name": "testsystem0"}, self.token)
        self.assertTrue(result)

    def _copy_distro(self):
        """
        Test: copy a distro object
        """

        tprint("copy_distro")
        distro = self.remote.get_item_handle("distro", "testdistro0", self.token)
        self.assertTrue(self.remote.copy_distro(distro, "testdistrocopy", self.token))

    def _copy_profile(self):
        """
        Test: copy a profile object
        """

        tprint("copy_profile")
        profile = self.remote.get_item_handle("profile", "testprofile0", self.token)
        self.assertTrue(self.remote.copy_profile(profile, "testprofilecopy", self.token))

    def _copy_system(self):
        """
        Test: copy a system object
        """

        tprint("copy_system")
        system = self.remote.get_item_handle("system", "testsystem0", self.token)
        self.assertTrue(self.remote.copy_system(system, "testsystemcopy", self.token))

    def _rename_distro(self):
        """
        Test: rename a distro object
        """

        tprint("rename_distro")
        distro = self.remote.get_item_handle("distro", "testdistrocopy", self.token)
        self.assertTrue(self.remote.rename_distro(distro, "testdistro1", self.token))

    def _rename_profile(self):
        """
        Test: rename a profile object
        """

        tprint("rename_profile")
        profile = self.remote.get_item_handle("profile", "testprofilecopy", self.token)
        self.assertTrue(self.remote.rename_profile(profile, "testprofile1", self.token))

    def _rename_system(self):
        """
        Test: rename a system object
        """

        tprint("rename_system")
        system = self.remote.get_item_handle("system", "testsystemcopy", self.token)
        self.assertTrue(self.remote.rename_system(system, "testsystem1", self.token))

    def _remove_distro(self):
        """
        Test: remove a distro object
        """

        tprint("remove_distro")
        self.assertTrue(self.remote.remove_distro("testdistro0", self.token))
        self.assertTrue(self.remote.remove_distro("testdistro1", self.token))

    def _remove_profile(self):
        """
        Test: remove a profile object
        """

        tprint("remove_profile")
        self.assertTrue(self.remote.remove_profile("testsubprofile0", self.token))
        self.assertTrue(self.remote.remove_profile("testprofile0", self.token))
        self.assertTrue(self.remote.remove_profile("testprofile1", self.token))

    def _remove_system(self):
        """
        Test: remove a system object
        """

        tprint("remove_system")
        self.assertTrue(self.remote.remove_system("testsystem0", self.token))
        self.assertTrue(self.remote.remove_system("testsystem1", self.token))

    def _get_repo_config_for_profile(self):
        """
        Test: get repository configuration of a profile
        """

        self.remote.get_repo_config_for_profile("testprofile0")

    def _get_repo_config_for_system(self):
        """
        Test: get repository configuration of a system
        """

        self.remote.get_repo_config_for_system("testprofile0")

    def test_distro_profile_system(self):
        """
        Test remote calls related to distro, profile and system
        """

        self._get_distros()
        self._create_distro()
        self._get_distro()
        self._find_distro()
        self._copy_distro()
        self._rename_distro()

        self._get_profiles()
        self._create_profile()
        self._create_subprofile()
        self._get_profile()
        self._find_profile()
        self._copy_profile()
        self._rename_profile()
        self._get_repo_config_for_profile()

        self._get_systems()
        self._create_system()
        self._get_system()
        self._find_system()
        self._copy_system()
        self._rename_system()
        self._get_repo_config_for_system()

        self._remove_system()
        self._remove_profile()
        self._remove_distro()
