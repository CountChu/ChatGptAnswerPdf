**You:**

https://genode.org/documentation/articles/trustzone

* * *

**ChatGPT:**

The link you've shared ([https://genode.org/documentation/articles/trustzone](https://genode.org/documentation/articles/trustzone)) directs to an article on Genode's website that discusses TrustZone technology. Genode is an open-source operating system framework focused on creating a secure and scalable environment for running multiple instances of software. TrustZone is a security technology developed by ARM, which is widely used in modern processors.

TrustZone technology aims to provide a secure execution environment for trusted applications, protecting them from potential security threats posed by untrusted applications. It achieves this by dividing the system into two distinct worlds: the "Secure World" and the "Normal World." These two worlds run concurrently on the same hardware, but they are isolated from each other, ensuring that sensitive data and operations remain protected.

The "Secure World" is designed to handle security-sensitive tasks, while the "Normal World" handles general-purpose tasks. To switch between the two worlds, ARM provides a secure monitor call (SMC) instruction that manages the transitions.

Genode leverages TrustZone technology to enhance the security of its operating system framework. By using TrustZone, Genode can isolate critical parts of the system and applications from the rest of the system, reducing the risk of sensitive data leaks or unauthorized access.

If you have any specific questions about TrustZone or Genode, feel free to ask, and I'll do my best to help.

* * *

**You:**

Please summarize the following articles in short.

* * *

**ChatGPT:**

It appears you forgot to provide the articles that you'd like me to summarize. Please provide the links or titles of the articles, and I'll be happy to provide summaries for you.

* * *

**You:**

An Exploration of ARM TrustZone Technology ARM TrustZone technology has been around for almost a decade. It was introduced at a time when the controversial discussion about trusted platform-modules (TPM) on x86 platforms was in full swing (TCPA, Palladium). Similar to how TPM chips were meant to magically make PCs "trustworthy", TrustZone aimed at establishing trust in ARM-based platforms. In contrast to TPMs, which were designed as fixed-function devices with a predefined feature set, TrustZone represented a much more flexible approach by leveraging the CPU as a freely programmable trusted platform module. To do that, ARM introduced a special CPU mode called "secure mode" in addition to the regular normal mode, thereby establishing the notions of a "secure world" and a "normal world". The distinction between both worlds is completely orthogonal to the normal ring protection between user-level and kernel-level code and hidden from the operating system running in the normal world. Furthermore, it is not limited to the CPU but propagated over the system bus to peripheral devices and memory controllers. This way, such an ARM-based platform effectively becomes a kind of split personality. When secure mode is active, the software running on the CPU has a different view on the whole system than software running in non-secure mode. This way, system functions, in particular security functions and cryptographic credentials, can be hidden from the normal world. It goes without saying that this concept is vastly more flexible than TPM chips because the functionality of the secure world is defined by system software instead of being hard-wired. The figure above illustrates the concept of the two worlds. The normal world is active (non-secure bit is set), the OS running on the platform can only access a subset of the physical resources. When a world switch takes place, the secure world comes into effect. The system software running in the secure world can access the devices hidden from the normal world. As former university researchers in the field of OS security, ARM TrustZone was deemed as relevant to us. We still have fond memories of a joint research project called ROBIN with STMicroelectronics where we could see the use of TrustZone on an ARM1176-based prototype platform for co-hosting Linux with an L4-based secure OS. However, since the project ended in 2008, we haven't heard much about this technology for several years. TrustZone seemed like one of so many obscure processor features that, once introduced into products, nobody could get really excited about. Well, in the case of TrustZone this is actually not true. In 2012, we were approached from different angles with questions about ARM TrustZone. It looked like, by then, TrustZone had become a kind of marketing term used by SoC vendors to sell confidence in the security of their chips. The term "TrustZone" appeared to be quite cloudy and it carried possibly wrong expectations and misconceptions with it. A lot of questions popped up: Does TrustZone provide mechanisms for secure booting and secure storage? Isn't it a kind of virtualization technology? If yes, isn't it superseded by ARM's virtualization extensions? How does it work? Is it important to consider it when developing an operating system? These questions prompted us to dive right into the world of TrustZone. We spent two and half years on and off with experimentation on several ARM platforms, each with a quite different interpretation of TrustZone-based security. This article summarizes our findings. Section Starting point describes the starting point of our journey and lays out the possible routes we considered to take. It is followed by Section The design and genesis of our custom base-hw kernel platform, which gives the rationale behind creating a custom kernel platform to support our undertaking. Section Hypervisor managing the non-secure world goes into detail about the TrustZone-specific challenges we faced while building a prototype. The actual prototype is covered by Section TrustZone demonstrated in color. Finally, the article summarizes our findings in a Q&A style in Section Common questions, answered.

* * *

**ChatGPT:**

Title: An Exploration of ARM TrustZone Technology

Summary: ARM TrustZone technology is a security solution for ARM-based platforms that introduces a "secure mode" alongside the regular "normal mode." The secure mode establishes a "secure world" and a "normal world" that run concurrently but are isolated from each other, ensuring that sensitive data and operations remain protected. TrustZone is more flexible than TPM chips because its functionality is defined by system software rather than being hard-wired. Despite initial skepticism, TrustZone has gained attention as a marketing term for SoC vendors to promote confidence in their chip's security. The article delves into various aspects of TrustZone, including its rationale, design, implementation, and common questions related to the technology.

* * *

**You:**

Starting point The first question on the table when starting a series of experiments was the one for a suitable development platform. At the time we started our investigations, we were most interested in the ARM Cortex-A9-based SoCs. All Cortex-A9 cores are equipped with ARM's security extensions (often referred to as TrustZone capabilities). In principle, any Cortex-A9 based platform would be suitable for us. However, even though there are many low-cost ARM development boards on the market (e.g., by Samsung, TI, ST-Ericsson, NVIDIA, ZiiLABS), we discovered that none of those options provided access to the secure mode of TrustZone. In almost all cases, bootstrap code stored in the ROM switches to non-secure mode prior starting the boot loader, possibly to prevent access to certain parts of the SoC that are not intended for public use. This narrowed the potential base platforms to FreeScale's i.MX development boards and the ARM Versatile Express platform. The FreeScale i.MX platform places no restrictions on the use of the secure mode. But at the time we started, no Cortex-A9-based board was available. The most recent board i.MX53 featured a single-core Cortex-A8 processor. The ARM Versatile Express Cortex-A9 board is the official reference board by ARM, which supports ARM TrustZone. As expected, the official reference board comes with a price tag far north of your usual low-cost development board. It's not that it is an order of magnitude more expensive. It's actually two orders! Still, we were happy to get our hands on one of those and could kick off our line of experiments on the official reference platform. We conducted two lines of experimentation: Prototyping using an existing microkernel and the creation of a custom kernel platform. The primary motivation for the former line of work was to have a low-risk path to enable the reference hardware and to get acquainted with the principle use of ARM Cortex-A9. By taking and modifying an existing kernel platform that is known to work on this CPU core, we had a good starting point. However, to get a thorough understanding of TrustZone's mechanisms, we needed to tackle problems that lay in the scope of the kernel. Furthermore, we desired to be in complete control over the bootstrapping procedure, in particular to address questions about secure booting. Rather than patching an existing kernel and inheriting its design choices, we decided to create a custom kernel platform that gives us all the freedom needed to explore the platform without having to consider the complexities of an existing kernel implementation. For both lines of work, we used the Genode OS Framework (Genode) as foundation. Genode is a construction kit for building special-purpose operating systems. It is a collection of small building blocks, out of which complex systems can be composed. Those building blocks include not only applications but all classical OS functionalities like kernels, device drivers, and protocol stacks. Currently, Genode supports 8 different kernels and provides over 100 reusable components for both x86-based and ARM-based platforms. We figured that its low trusted computing base (TCB) complexity yet high flexibility would make it an attractive foundation for an OS designated to run on the secure side of TrustZone. For the first line of work, the enablement of the Versatile Express platform, one of the kernels L4/Fiasco, Fiasco.OC, or Codezero were principally suitable. Of these candidates, Fiasco.OC provided the broadest support for the most recent ARM SoCs. Hence, we decided to use the combination of Genode with Fiasco.OC as starting point to enable the principal use of Genode on the platform. This required us to implement low-level driver support for basic peripherals such as the PL110 display, the PL011 UART, timer, and PS/2. Even though the driver-related work was conducted using the Fiasco.OC kernel, the outcome was beneficial for both lines of work Fiasco.OC and our custom kernel as Genode's driver components are independent from the underlying kernel. In our second line of work, we supplemented Genode with a new base platform that we call "base-hw" ("hw" representing Genode running on bare hardware). In contrast to the already supported kernels, this new platform is tightly integrated with the core of Genode. Thereby, we aimed to dramatically reduce the TCB complexity of the base system compared to the use of a discrete kernel. The most significant benefit of the custom kernel platform in the context of our TrustZone experimentation are the insights into kernel-level problems when using the Cortex-A9 and TrustZone.

* * *

**ChatGPT:**

Title: Starting Point and Experimentation with ARM TrustZone Technology

Summary: The article discusses the process of choosing a suitable development platform for exploring ARM TrustZone technology. It narrows down to the ARM Versatile Express Cortex-A9 board, an official reference board by ARM. Two lines of experimentation are conducted: prototyping using an existing microkernel and creating a custom kernel platform. Genode OS Framework is used as the foundation for both lines of work, due to its low trusted computing base complexity and high flexibility. The first line of work uses the combination of Genode with Fiasco.OC to enable the principal use of Genode on the platform, while the second line of work supplements Genode with a new base platform called "base-hw" to reduce the TCB complexity of the base system and gain insights into kernel-level problems when using Cortex-A9 and TrustZone.

* * *

**You:**

The design and genesis of our custom base-hw kernel platform In contrast to classical L4 microkernels where Genode's core process runs as user-level roottask on top of the kernel, base-hw executes Genode's core directly on the hardware with no distinct kernel underneath. Core and kernel are melted into one novel kind of hybrid kernel/userland program. Only a few code paths are executed in privileged mode but most code runs in user mode. This design has several benefits. First, the kernel part becomes much simpler. For example, there are no allocators needed in the kernel part because allocators are managed by the user-level part of core. Second, base-hw side-steps long-standing hard kernel-level problems, in particular the management of kernel resources. For the allocation of kernel objects, we can simply employ Genode's user-level resource trading concepts. Finally and most importantly, however, merging the kernel with roottask removes a lot of redundancies between both programs. Traditionally, both kernel and roottask performed the book keeping of physical-resource allocations and the existence of kernel objects such as address spaces and threads. In base-hw, those data structures exist only once. The complexity of the combined kernel/core is significantly lower than the sum of the complexities of a traditional self-sufficient kernel and a distinct roottask on top. This way, base-hw helps to make Genode's TCB less complex. The figure illustrates the effect of the new design on the TCB of the root of Genode's process tree. On the left, a traditional member of the L4 family of kernels is depicted. The bluish marked TCB comprises the kernel, the sigma0 root memory manager, roottask (Genode's core), and Genode's init process. These components accumulate to circa 60 thousand lines of code. On the right, the hybrid core/kernel approach of base-hw is illustrated. By merging the kernel with roottask, systems running on top of base-hw need to trust less code to be void of bugs. For realizing the base-hw kernel platform, we undertook the following steps. First, we designed and implemented the concept for bootstrapping a Genode-based system consisting of potentially many modules as a single boot image. This is the first point where using a custom platform over a stock Fiasco.OC kernel turned out to be beneficial because our boot concept is extremely simple compared to the procedure known from Fiasco.OC. The kernel entry and exit code paths had been implemented and tested on both Qemu and the reference hardware. The execution model of the kernel can be roughly characterized as a single-stack kernel. In contrast to traditional L4 kernels that maintain one kernel thread per user thread, the base-hw kernel is a mere state machine that never blocks in the kernel. This is similar to how the seL4 kernel and the NOVA microhypervisor operate. The next step was to add support for interrupt handling and preemptive multi-threading. So we implemented drivers for the PL390 interrupt controller and the Cortex-A9 core timer. Combined with the implemented kernel-entry code path and the interrupt controller, timer interrupts could be handled by Genode's user-level core. Genode's core component uses multiple threads of execution: The main thread that initializes the platform and spawns the first user-level process called init, A pager thread that receives and handles page faults, One thread per device interrupt, A so called RPC entrypoint that handles requests to the services provided by core, and The parent thread of the init process that responds to requests of the init process via the parent interface. Because the correct functioning and scheduling of those threads is fundamental for bringing-up of the system, the next logical step was the introduction of a preemptive scheduler and core-local context switching. Core-local threads do not run independently but interact with each other via synchronous inter-process communication. For example, the main thread creates the RPC entrypoint and then acts as a client of some core services. To accommodate those use cases, the kernel interface was supplemented with system calls for synchronous inter-process communication (IPC). To keep the kernel as simple as possible, IPC is performed using so-called user-level thread-control blocks (UTCB). Each thread has a corresponding memory page that is always mapped in the kernel. This UTCB page is used to carry IPC payload. The largely simplified procedure of transferring a message is as follows. (In reality, the state space is more complex because the receiver may not be in a blocking state when the sender issues the message) The user-level sender marshals its payload into its UTCB and invokes the kernel, The kernel transfers the payload from the sender's UTCB to the receiver's UTCB and schedules the receiver, The receiver retrieves the incoming message from its UTCB. Because all UTCBs are always mapped in the kernel, no page faults can occur during the second step. This way, the flow of execution within the kernel becomes predictable and always returns to the user land. In addition to IPC, threads interact via the synchronization primitives provided by the Genode API. To implement these portions of the API, the kernel was then enhanced with system calls for managing the execution control of threads. With the entity of core running on the reference platform, it was time for spawning the first non-core user-level process, namely the init process. This process is a composition out of multiple core sessions: A CPU session with the main thread of the init process, A region-manager (RM) session describing the address space of the process, A protection-domain (PD) session representing the encapsulation boundary of the process, A RAM session containing the physical memory resources available to the init process. To accommodate the implementation of these services, the kernel was enhanced with system calls that handle protection domains and page faults at user level. At the startup of the init process, its first life sign is a page fault produced by the main thread on the attempt to fetch its first instruction. The kernel translates this page fault into an IPC message to the pager thread. In contrast to core-internal IPC, this cross-PD-IPC requires the kernel to not only switch thread contexts but also address spaces. All further functionalities needed to bring up the init process such as the ELF loading were readily provided by the generic code of the Genode OS Framework. The last step towards executing real-world application scenarios on our custom kernel was the provisioning of mechanisms required by user-level device drivers. Those mechanisms are memory-mapped I/O access and IRQ delivery, which are provided via core's IO\_MEM and IRQ services. To implement those services, the kernel had to be supplemented with system calls for allocating and receiving IRQs. With those functionalities in place, the path was cleared to execute user-level device drivers that we already had enabled when using the Fiasco.OC kernel, i.e., drivers for the user-level timer, framebuffer, and PS/2 input devices. Thereby, we became able to run a basic graphical interactive demo scenario on our custom kernel. For more sophisticated work loads that require asynchronous communication, we subsequently improved the kernel mechanisms. For example, we added kernel-level support for Genode's signalling API and thereby achieved full coverage of the Genode API on our custom kernel platform.

* * *

**ChatGPT:**

Title: Design and Genesis of Custom Base-HW Kernel Platform for Genode

Summary: The custom base-hw kernel platform for Genode features a unique hybrid kernel/userland design that simplifies the kernel part, side-steps hard kernel-level problems, and reduces redundancies between kernel and roottask, ultimately resulting in a lower trusted computing base (TCB) complexity. The platform was developed in several steps, including designing and implementing the bootstrapping concept, kernel entry and exit code paths, support for interrupt handling and preemptive multi-threading, core-local context switching, inter-process communication, and user-level device driver mechanisms. This custom kernel platform enabled the execution of real-world application scenarios and provided full coverage of the Genode API.

* * *

**You:**

Hypervisor managing the non-secure world This section describes our experiences while creating a TrustZone-aware hypervisor that is able to schedule between one non-secure virtual-machine (VM), and multiple tasks running unprivileged in secure mode. Based on our custom base-hw kernel platform, it describes the consecutive steps that were taken to turn the kernel into a TrustZone-aware hypervisor, as well as to build a virtual-machine monitor (VMM) running as user-level component on top of that kernel.

* * *

**ChatGPT:**

Title: TrustZone-Aware Hypervisor for Managing the Non-Secure World

Summary: A TrustZone-aware hypervisor was developed for managing one non-secure virtual machine (VM) and multiple tasks running unprivileged in secure mode. The hypervisor was built upon the custom base-hw kernel platform and involved several steps, including making the kernel TrustZone-aware and constructing a virtual machine monitor (VMM) as a user-level component on top of the kernel. The hypervisor was designed to seamlessly schedule between the non-secure VM and secure tasks, providing a robust and secure foundation for managing different security domains in a TrustZone-enabled system.

* * *

**You:**

World switch between non-secure world and secure world We started investigating TrustZone by bringing the so called monitor-mode in the Genode/ARM-kernel to life. The monitor mode is an execution mode add-on in ARM CPUs implementing the Security Extensions (SE is equivalent to TrustZone). It is an execution mode (like e.g., system, user, or supervisor mode), the CPU switches to when certain exceptions occur. For most of the exceptions, the CPU can be configured whether it raises an exception in monitor-mode, or in the corresponding exception mode of the non-secure or secure-world. A so-called Secure Configuration Register (SCR) enables the hypervisor to configure whether the CPU should trap when fast interrupts, or normal interrupts, or external data aborts occur, while the non-secure world is active. In addition to interrupt-triggered mode switches, the non-secure world is able to explicitly enter the monitor mode by the means of a software-generated exception via the smc instruction. So the first step was to initialize a corresponding exception vector that is used when a monitor-mode exception is raised. Thereby, our consideration was that all exceptions that enter the monitor mode should be triggered by the non-secure world only, but never by the secure world. Given that assumption, the we designed the exception vector in a way that it always stores the current CPU state as a non-secure world's state. The CPU state is saved regardless of the type of exception. In addition to the CPU state, the exception type is stored in the same area. On the switch to the monitor mode, the kernel reloads the formerly stored secure kernel-context from a known memory area. Given this approach, the software stack running in the secure world must not execute the smc instruction. This drastically simplifies the assembler world-switch routine. In application scenarios where a subset of components executed in the secure world are untrusted, it is principally possible to extend the world-switch routine to check for the world that raised the fault. In general, the monitor-mode exception vector works orthogonal to the kernel-/user-mode switch. In contrast to that, the world-switch has to save/restore more register banks. To switch from the secure to the non-secure world the symmetrical operations are also performed, only that this time, the world switch is not triggered by an exception but via a newly introduced system call with a pointer to the VM's CPU state. The kernel responds to this system call by pushing the provided state to the non-secure world.

* * *

**ChatGPT:**

Title: World Switch Between Non-Secure and Secure Worlds

Summary: A world switch mechanism was implemented to facilitate transitions between the non-secure and secure worlds in a TrustZone-enabled system. The monitor mode was utilized, which is an execution mode add-on in ARM CPUs with Security Extensions (TrustZone). The system is designed so that all exceptions entering the monitor mode should be triggered only by the non-secure world, simplifying the assembler world-switch routine. The secure world can switch back to the non-secure world through a system call with a pointer to the VM's CPU state, pushing the provided state to the non-secure world.

* * *

**You:**

User-level Virtual Machine Monitor (VMM) To be able to use the newly introduced system call that switches to the non-secure-world, we introduced a new VM-session interface as service in Genode's core. This interface enables a client (VMM) to affect the whole CPU state of a VM, initiate a world switch to the non-secure world, and, after an exception-triggered return, to obtain the VM's state. Moreover, the new interface enables a client to obtain a portion of physical RAM as I/O memory, so that it can prepare it as the VM's physical RAM. Moving this physical RAM portion into the I/O memory allocator of core allows the VMM to get the appropriate RAM portion to load the VM's ELF image to its physical relocation address. The image above illustrates the relationship between the user-level VMM (TZ VMM) and Genode's core/kernel. TZ VMM initiates the switch to the normal world by invoking the run function of the VM session interface. The normal world is scheduled as a (low-priority) thread by the base-hw kernel. Given the world-switch routine in the kernel and the VM-session interface of core, all prerequisites were in place to build a first simple version of a VMM. This version solely acquires some portion of RAM, takes a ROM module (the VM's image to load), and loads the ELF binary to physical RAM. During ELF-loading, it identifies the correct entry point, and sets the program counter of the VM's CPU state accordingly. Finally, the VMM enters an endless loop where it executes the VM and, after each exceptional return, dumps the VM's CPU state to the debugging console.

* * *

**ChatGPT:**

Title: User-Level Virtual Machine Monitor (VMM)

Summary: A new VM-session interface was introduced as a service in Genode's core to enable a client (VMM) to manage the CPU state of a VM, initiate a world switch to the non-secure world, and obtain the VM's state. This allows the creation of a simple VMM that acquires a portion of RAM, loads the VM's ELF binary to physical RAM, and sets the program counter of the VM's CPU state. The VMM enters an endless loop, executing the VM and dumping its CPU state to the debugging console after each exceptional return.

* * *

**You:**

Simple test kernel for the non-secure world To test the newly implemented world-switch routine, we created a simple test kernel was. It is built almost entirely out of assembler code, which performs the following steps: Setup exception vectors for data-aborts, pre-fetch aborts, interrupts, fast-interrupts, supervisor-calls, Initialize interrupt controller to receive UART0 interrupts, Initialize UART0 to be able to print simple messages, and detect interrupt reception (RX), Switch to user-mode and idle, Whenever an interrupt occurs print some short message. TrustZone Platform Controller (TZPC) and Address-Space Controller (TZASC) After successfully testing the VMM setup and the world-switch routine, it was time to investigate TrustZone mechanisms, which actually protect the secure world from the non-secure world. A set of different IP cores exists beside the CPU core, which helps to confine the non-secure software stack. With respect to the Versatile Express platform, these are the following: TrustZone Protection Controller (TZPC) TrustZone Address Space Controller (TZASC) The Cortex A9 MPCore internal Interrupt Controller The first and easiest part seemed to be the configuration of the physical memory areas that should be preserved for the secure world but invisible to the non-secure world, i.e., the RAM where the secure software stack is located in. The bus and memory hierarchy in modern embedded architectures, like in the Versatile Express Motherboard/Daughterboard conglomerate, is highly complex. It consists of different bus systems (ABP, AXI), memory controllers (SMC, DMC), and caches. Most of the controllers and devices in this jungle are not TrustZone aware themselves but are protected by the TZPC or TZASC. Given the sparse public information available in technical reference manuals, it was hard to identify, which components can be protected and how the TZPC/TZASC are related to them. Due to experimentation, we were able to deduct the following insights. The TZASC controller on the platform is used to secure physical address ranges that are addressable through the Static Memory Controller (SMC). In principal, it should be possible to secure another memory controller by a TZASC too, but on the platform, it is restricted to the SMC. These physical address regions correspond to the I/O resources of peripheral devices, some SRAM, and flash memory. Most of these components are placed on the motherboard. The DDR RAM on the other hand is not subjected to the SMC, but sits behind the Dynamic Memory Controller (DMC), which is not protected by any TZASC. With the help of the TZASC, it is possible to define multiple regions as secure or non-secure. However, these definitions do not apply to DDR RAM. The TZPC is used to protect on-chip peripherals (e.g., the TZPC and TZASC themselves) as well as bus accesses to external subsystems. Thereby, one can configure whether access to a corresponding on-chip device is allowed. For example, one bit in the TZPC is reserved to enable or disable access to the DMC from the non-secure world. The TZPC doesn't allow a more fine-grained confinement with respect to a single device, like for instance the DMC. Given those findings, the Versatile Express platform apparently does not allow the partitioning of DDR RAM into secure and non-secure address ranges. One can only decide to assign it to either of both worlds. SRAM and flash-memory on the other hand, which are under control of the TZASC, can be configured more fine-grained. Furthermore, when running an unmodified Linux software stack in the non-secure world, we need to assign the entire DDR RAM to the non-secure world. Fortunately, the platform hosts 32 MiB of SRAM, which we can preserve for the exclusive use by the secure world.

* * *

**ChatGPT:**

Title: Simple Test Kernel for Non-Secure World & TrustZone Platform and Address-Space Controller

Summary: A simple test kernel was created to test the VMM setup and the world-switch routine. TrustZone mechanisms were investigated to protect the secure world from the non-secure world. The Versatile Express platform features TrustZone Protection Controller (TZPC) and TrustZone Address Space Controller (TZASC). The TZASC controller is used to secure physical address ranges addressable through the Static Memory Controller (SMC), and the TZPC protects on-chip peripherals and bus accesses to external subsystems. The platform does not allow the partitioning of DDR RAM into secure and non-secure address ranges, but it does host 32 MiB of SRAM that can be preserved for exclusive use by the secure world.

* * *

**You:**

Interrupts In the previous section, we identified how to partition the physical resources of the reference platform into two worlds by assigning memory-mapped I/O (MMIO) resources of peripherals to either of both worlds. However, access to MMIO is only the half way towards the practical use of these peripherals. We also need a way to route the corresponding device interrupts to the respective worlds. Unfortunately, the assignment of device interrupts to either the secure or non-secure world cannot be configured directly. Instead, it is merely possible to distinct the handling of normal interrupts (IRQ) and fast interrupts (FIQ). The ARM architecture defines these two types, which differ in the following ways: Each type has a unique exception vector so that FIQs enter the kernel using a different code path than IRQs. On the occurrence of an IRQ, the CPU automatically saves a more comprehensive register state compared to an FIQ. The most distinctive characteristic is that an FIQ can preempt any exception handler except for the FIQ handler. So exceptions can nest. For a device interrupt, it is possible to define whether to take the IRQ or FIQ exception entry in the PIC configuration. This mechanism indirectly enables the partitioning of interrupts between both worlds by configuring the PIC to use FIQs for secure and IRQs for the non-secure world exclusively. Using the Secure Configuration Register, it is possible to revoke the use of FIQs from the non-secure world and force a trap into the monitor for each FIQ that occurs while the non-secure mode is active. To implement this idea, we modified our custom kernel to handle FIQs instead of IRQs, which is slightly more complicated because of the possible nesting of exceptions. We solved the problem of nested exceptions by checking for the originating CPU mode that was active when the FIQ occurred. If the CPU was already in kernel mode, we can conclude that the exception refers to a nested exception. In this case, we ignore the FIQ and fall back to resuming the previous exception. To summarize the above, FIQs are exclusively used by the device drivers of the secure world whereas IRQs are exclusively used by the non-secure world (as expected by the Linux kernel). Because for each device, we can define whether its interrupts are delivered as FIQs or IRQs, we are thereby able to assign individual device interrupts to either of both worlds.

* * *

**ChatGPT:**

Title: Interrupts in Secure and Non-Secure Worlds

Summary: Device interrupts can be indirectly partitioned between the secure and non-secure worlds using the ARM architecture's two types of interrupts: normal interrupts (IRQ) and fast interrupts (FIQ). The custom kernel can handle FIQs for the secure world and IRQs for the non-secure world. By defining whether a device's interrupts are delivered as FIQs or IRQs, it is possible to assign individual device interrupts to either the secure or non-secure world. This setup allows secure world device drivers to use FIQs exclusively while IRQs are used by the non-secure world, as expected by the Linux kernel.

* * *

**You:**

Booting Linux in the non-secure world Having the principal separation between the secure and non-secure world in place, we can now replace our simple custom non-secure kernel with the Linux kernel. This work comprises the following steps: Loading the kernel. The kernel has to be complemented with additional boot-time information called ATAGs. The ATAGs data structure contains the location of the RAM, the address of the RAM disk as well as the kernel command line. In addition to the kernel, a RAM disk must be loaded into the memory of the non-secure world. This RAM disk contains the initial boot image. To test the loading procedure, we started Linux with all access rights to the peripherals granted and observed the successful boot-up of the kernel. At this point, we disabled the access to all peripherals and entered the iterative process of booting the kernel, looking where it hangs because of a missing permission, and then taking one of the following decisions: For devices that we deemed as uncritical for the secure world, we would grant direct device access. For devices that must be preserved for the secure world, we slightly changed the Linux kernel code to issue a hypercall instead of accessing the device resource directly. When the non-secure OS issues a hypercall using the smc instruction, the CPU enters the monitor mode and passes control to the hypervisor. The hypervisor reflects that hypercall to the user-level VMM, which is able to respond to the individual hypercalls. Those hypercalls are: SP810\_ENABLE Enable the timer. CPU\_ID: Request the CPU ID, which is the hard-coded value 0x0c000191 for the reference platform. SYS\_COUNTER Returns the value of the Sys\_24MHz system register. MISC\_FLAGS Returns the value of the Sys\_misc system register. SYS\_CTRL Perform one of the system configuration control operations OSC1, DVI\_SRC, and DVI\_MODE. MCI\_STATUS Returns the value of the Sys\_mci system register. We would have preferred to employ a trap-and-execute emulation scheme for those register accesses. However, as described in the following section, this technique is not feasible with the mechanisms provided by TrustZone.

* * *

**ChatGPT:**

Title: Booting Linux in the Non-Secure World with TrustZone

Summary: To boot Linux in the non-secure world using TrustZone, a Linux kernel and a RAM disk must be loaded into memory. The kernel is complemented with ATAGs data structure, which contains essential boot-time information. To ensure security, access to peripherals is granted or denied based on their criticality for the secure world. For devices that must be preserved for the secure world, the Linux kernel code is modified to issue hypercalls instead of directly accessing device resources. The hypervisor reflects these hypercalls to the user-level VMM, which responds to them accordingly.

* * *

**You:**

Device emulation We considered device emulation as a less intrusive alternative to the introduction of hypercalls. In contrast to the hypercall approach, device emulation does not require us to change the Linux kernel. The basic idea of emulating device access is to let the hypervisor pass control to the VMM as soon as the non-secure OS accesses an address outside the permitted physical address ranges. The VMM can then inspect the address in question and the program counter of the non-secure OS that raised the access violation. Given the program counter value, the VMM can fetch and decode the faulting instruction and emulate it in software. Because ARM is a RISC architecture, the instruction decoding is rather simple. The instruction in question can only be a load or a store instruction. No other instruction would raise an access fault. For read operations, the VMM would provide the result of the operation by changing the corresponding entry of the VM state structure. That said, we found that the trap-and-execute emulation model is not possible to implement with the TrustZone protection mechanisms in general. Dependent on the concrete platform, the CPU will not immediately enter the hypervisor when the fault occurs but attempts to perform the bus transaction. This transaction will trigger an external data abort. This abort is similar to a device interrupt. It principally raises an exception (so the violation can be detected) but not always immediately. Therefore, there is no way to uniquely reconstruct what happened in between the invalid access and the reception of the external abort exception in the hypervisor. Neither can the hypervisor recover the non-secure world to a useful state. The image above displays the flow of control when the normal-world OS performs an illegal device access. The Genode system starts in the secure world. The user-level TZ VMM component bootstraps the rich OS, and finally control to the normal world via the run function of the kernel, which, in turn, initiates a world switch to the normal world. If the rich OS accesses a device, which was not assigned to the normal world, an external data abort occurs, and control is passed back to the secure world. The virtual device model may try to trap-and-execute the faulting instruction. We found that the latency of reporting access violations can be reduced by adding memory barriers to the faulting code. However, as this comes down to changing the Linux kernel, this would defeat the initial incentive for using device emulation instead of introducing hypercalls. The general pattern of changing the original code to using a hypercall looks as follows (ctr refers to a critical device register): +#ifdef RUNS\_IN\_SECURE\_WORLD if (ctr) return readl(ctr); +#else + if (ctr) { + static u32 ret; + asm volatile("mov r1, #3 \\n" + "dsb \\n" + "dmb \\n" + "smc \\n" + "mov %\[value\], r0 \\n" : \[value\] "=r" (ret) :: "r0", "r1"); + return ret; + } +#endif We replaced the original call to the access function readl(ctr) with the snippet above. A ready-to-use configuration for the Linux kernel accompanied with the needed modification to the kernel source code are available here: Adaptation of the Linux kernel https://github.com/skalk/linux/commit/284073c4f6c0e6a77c02ae9d296da9c46f6f5104.patch We tried to keep the kernel patch as small as possible. The patch comprises the addition of only 73 lines of code (6 hypercalls) to the kernel. With these few modifications, we were able to boot Linux completely in the non-secure world.

* * *

**ChatGPT:**

Title: Device Emulation in TrustZone's Non-Secure World

Summary: Device emulation in the non-secure world using TrustZone is considered as an alternative to introducing hypercalls. However, trap-and-execute emulation is not feasible due to the latency in reporting access violations. Instead, modifications to the Linux kernel are made by replacing calls to access functions with hypercalls, allowing Linux to boot completely in the non-secure world. A minimal kernel patch was developed to achieve this, only adding 73 lines of code and enabling the successful boot of Linux in the non-secure world.

* * *

**You:**

TrustZone demonstrated in color The goal of our ARM TrustZone experiments was to push the envelope of this technology beyond the typical scope of TPM-like functionality on a mobile tablet device. We aimed at executing a complete Genode-based operating system in the secure world while running a largely unmodified Android OS in the normal world. The secure OS does not merely sit in the background but comes with a graphical user interface that responds to user input via the touchscreen. At any time, the user is able to switch between both worlds using a button. We identified the Freescale i.MX53 SABRE tablet as a suitable platform for this experiment. It is one of the few ARM development platforms that allows the developer to access the secure world of TrustZone and it has a tablet form factor. As we performed our initial TrustZone-related research on the ARM Versatile Express platform, we were furthermore interested in learning more about the differences of the TrustZone implementations of two different SoC vendors. The practical work consisted of the following steps: Adaptation of Genode to the i.MX53 platform, Enabling TrustZone on i.MX53, Implementing a TrustZone monitor that deals with the specifics of the i.MX53 with the goal of booting Linux in the normal world besides Genode, Display driver running as user-level device driver on Genode Touchscreen driver running as user-level device driver on Genode Interfacing Genode's display and user-input drivers with the Android software stack. Multiplexing the display between Android and Genode using hardware overlays. In the following, each of those topics is briefly covered. Genode on i.MX53 SABRE tablet We conducted our first TrustZone experiments on the ARM Versatile Express platform based on a Cortex-A9 CPU. With Freescale i.MX53, we took the challenge to transfer our results to an entirely different platform. We considered two variants of a i.MX53-based platform. The so-called Quick-Start Board (QSB) is a low-cost development board whereas the SABRE-tablet reference platform comes in the form factor of a tablet. The principle adaptation of Genode to the new platform required us to add support for the Cortex-A8 CPU to our kernel and add device drivers for the i.MX-specific interrupt controller, UART, GPIO, and EPIT timer. With these adaptations, simple Genode scenarios could be executed on the platform. TrustZone on i.MX53 As the i.MX53 SoC is based on a Cortex-A8 CPU instead of a Cortex-A9 as used on the Versatile Express platform, we expected the need of minor changes to the TrustZone world-switching code. One particular i.MX-specific difference is the routing of interrupts. Because i.MX does use a custom interrupt controller, the assignment of interrupts to either the secure or the normal world works slightly differently than on the ARM Versatile Express platform. Furthermore, the i.MX53 comes with a custom TrustZone protection controller called Central Security Unit (CSU). Similar to the TrustZone protection controller used on the Versatile Express platform, the CSU allows the assignment of device groups to the secure or normal worlds using corresponding configuration bits. The CSU differentiates 64 device groups. Subsuming the individual devices to differentiable groups is up to the SoC vendor. A noteworthy advantage of the CSU compared to the ARM TZ protection controller within the ARM Cortex A9 reference board is the way of how access violations are handled. As stated in Device emulation, the ARM TZ protection controller responds to invalid accesses with an asynchronous external abort exception, similar to a device interrupt. Upon the execution of an offending instruction, the TZ protection controller detects the violation, yet the CPU would continue the execution of further instructions until the flagged violation eventually reaches the CPU, triggering an external abort exception. This scheme effectively rules out any attempt to emulate device accesses. In contrast, the i.MX CSU responds to access violations by synchronously yielding control to the exception handler. So when such an exception occurs, the offending instruction can be determined and emulated in software. However, even though device emulation using the CSU is principally possible, we haven't investigated this opportunity further. The second distinctive property of i.MX53 compared to the Versatile Express platform is the so-called Multi-Master Multi-Memory Interface (M4IF), which is part of the DDR memory controller. On the Versatile Express platform, we used 32 MiB SRAM for Genode and assigned the platforms DDR memory to the normal world. On i.MX53, this scheme would not work because there is no substantial amount of memory available besides the DDR RAM. This rules out a mere partitioning of memory using the CSU. However, the M4IF enables the masking of DDR RAM resources such that particular ranges can be preserved for the exclusive access by the secure world. We successfully used the M4IF to partition the DDR RAM between the secure world and the normal world. TrustZone monitor The user-level TrustZone monitor (we call it VMM because it acts very similar to a virtual machine monitor) for the i.MX53 had to be developed from scratch. Almost no code of the Versatile Express platform could be reused. To us, this experience is a valuable insight into the TrustZone technology. Even though the principle TrustZone mechanism for dividing control between both worlds is unified, it is up to the SoC vendor to implement their respective interpretation of security. I.e., the assignment of devices to the bits of a protection controller, the signalling mechanism for violations, the handling of the NS bit by the devices, or additional TZ-related bus components are not standardized. Hence, the mere claim that a product uses TrustZone does not automatically imply the presence of any meaningful security mechanisms. This is unfortunate if the use case of a product has not been envisioned by the SoC vendor. For example, in most application scenarios, TrustZone is used as a TPM-like component that is explicitly called by the normal world. It does not become active on its own. In our case, however, the secure world executes a complete OS including a preemptive scheduler. Therefore, access to clock and power management becomes critical in our scenario. Unfortunately, the clock and power management module does not support the protection of selected clocks and regulators from the normal world. The whole module can be either assigned to the normal world or the secure world. In the former case, the liveliness of the secure would would depend on the normal world. The latter case would require the implementation of extensive device-emulation code to use an unmodified OS kernel in the normal world. For our prototype, we partitioned the platform where easily feasible (e.g., for DDR memory, interrupts) but we did not attempt to implement device emulators. In the case of the clock and power management module, we decided to grant the normal world access to the devices, yet disabled code paths in the Linux kernel that would interfere with the liveliness of secure world. We feel that this approach is appropriate for a demonstrator. For building a real product, the decision would come down to an even-handed judgement. The hypercalls implemented by the i.MX53-specific VMM are related to the access of a few platform features that must not be handed to the normal world directly, in particular the virtual framebuffer and the virtual touchscreen.

* * *

**ChatGPT:**

Title: TrustZone Demonstrated on i.MX53 SABRE Tablet with Genode OS

Summary: The ARM TrustZone technology was utilized to execute a complete Genode-based operating system in the secure world and an unmodified Android OS in the normal world on an i.MX53 SABRE tablet. The secure OS included a graphical user interface with touchscreen interaction, allowing the user to switch between both worlds. Adaptations were made to Genode for i.MX53, and a TrustZone monitor was implemented to deal with the platform's specific requirements. The display was multiplexed between Android and Genode using hardware overlays, successfully demonstrating the capabilities of TrustZone beyond typical TPM-like functionality.

* * *

**You:**

Additional device drivers In addition to the low-level drivers outlined above, the demonstration scenario required us to implement a number of peripheral device drivers, in particular a framebuffer driver for the LCD display, a touchscreen driver, and a driver for responding to the capacitive sensors of the SABRE tablet. The task of creating the drivers, in particular the framebuffer driver, turned out to be more complex than anticipated. Even though we had documentation for the Image Processing Unit (IPU) available, the device is enormously complex. The specification of the IPU is around 1000 pages. In order to focus on parts that are relevant for us, we turned to analysing register traces of the driver that ships with the vendor's kernel. Unfortunately, we found the driver code to be extremely shaky and prone to race conditions. For example, added instrumentation code that slightly slowed down the register accesses performed by the driver would result in a defective driver. We were eventually able to pin-point the problem to a few critical register-access patterns but this had been a long-winding endeavour. Compared to the framebuffer driver, enabling the touchscreen device was a smooth experience with no major surprises. With both framebuffer driver and the touchscreen driver in place, we could successfully run Genode's Nitpicker GUI server on the SABRE tablet. However, in the naive implementation, Nitpicker would need to copy pixels of its GUI clients to the physical frame buffer via software-blitting. Even though we have assembly-optimized blitting routines for ARM in place, we expected a significant performance overhead of running Android as a Nitpicker client compared to the native execution of Android without any indirection. For this reason, we investigated the use of hardware overlays. Similar to most embedded graphics devices, the i.MX53 Image Processing Unit (IPU) comes with the ability to compose the final image from a number of so-called hardware overlays. Each overlay is fed by a stream of pixels fetched via DMA. The physical pixel color is the result of a compositing function that is evaluated per pixel. This function could give preference to one particular overlay, with the effect that the respective overlay is always displayed on top of all others. Alternatively, color keying can be used to decide which overlay is visible at a given screen position. The IPU can even mix colors of different overlays (alpha blending). Because the IPU fetches the pixels directly from memory using DMA and the pixel compositing function is executed in hardware, the display multiplexing can effectively be offloaded from the ARM CPU. Since we wanted to run Android at almost-native performance in the normal world, we found that the use of hardware overlays was mandated. Unfortunately, the exploration of the hardware-overlaying feature of the i.MX53 IPU turned out to be highly complex so that we had to invest significant development time into enabling this feature on the Quick Start Board, just to find out that this feature behaves differently on the SABRE tablet. Because there seems to be almost no community of users of the SABRE tablet platform, we were not able to leverage any public community knowledge while working on this. We eventually discovered that the order of seemingly loosely related register accesses was the tipping point for the driver to reach a functional state. With our custom IPU driver with hardware-overlay support in place, the seemed to be paved to securely multiplex the display between (untrusted) Android running in the normal world and Genode's Nitpicker GUI server running in the secure world. Because the access to the IPU and GPU from either of both worlds can be individually configured in the i.MX53 CSU, we could assign the IPU exclusively to the secure world while handing out the GPU to the normal world. This way, Android can leverage hardware-accelerated graphics while the secure world retains control over the display. Unfortunately, however, the TrustZone implementation of the i.MX53 SoC has a limitation that renders the isolation between IPU and GPU ineffective. From the investigation by security researchers of SRLabs, we learned that even though the CSU could be configured to restrict the access from either of worlds to the devices individually, there is no way to individually restrict the access from each of the devices to the secure and normal worlds. Both devices IPU and GPU require direct memory access (DMA) to operate. The IPU uses DMA to fetch pixels from the frame buffer. The GPU uses DMA to access GPU buffer objects (containing textures, shaders, vertex arrays) and the target surface of rendering operations. On the i.MX53, it is not possible to configure DMA access of IPU to the memory of the secure world while restricting DMA operations of the GPU to the normal world's memory. In fact, both devices IPU and GPU share the same DMA channel ID. Consequently, we had to grant DMA access from both devices to the memory of both worlds. This way, the normal world is actually able to compromise the secure world using DMA via the GPU. Thanks to SRLabs for this valuable insight! To fix this security hole, the SoC would either need to separate the DMA policy of both devices or the secure would would need to virtualize the GPU.

* * *

**ChatGPT:**

Title: Implementing Additional Device Drivers and Addressing TrustZone Limitations on i.MX53 SABRE Tablet

Summary: Additional device drivers were required for the ARM TrustZone demonstration on the i.MX53 SABRE tablet, including a framebuffer driver for the LCD display, a touchscreen driver, and a capacitive sensor driver. While developing the framebuffer driver proved to be more complex than anticipated, the touchscreen driver was implemented without major issues. Hardware overlays were employed to allow Android to run at near-native performance in the normal world, but TrustZone implementation limitations regarding the isolation between the Image Processing Unit (IPU) and GPU were discovered. To fix the security hole, the SoC would need to separate the DMA policy of both devices or the secure world would need to virtualize the GPU.

* * *

**You:**

Demonstration scenario Architectural overview of the TrustZone demo on i.MX53 Figure 6 presents an overview of the key components of the demonstration scenario. Dashed lines symbolize information flow. Solid lines represent a relationship of control. At boot time, Genode's core sets up the CSU configuration and thereby defines the permissions of the normal world to access peripherals. The CSU is configured such that security-critical peripherals such as the IPU and the touch screen controller are preserved for the secure world only. Not all relevant devices are depicted (e.g., timers and GPIO controller are omitted in the picture). After platform initialization, core spawns the Genode process tree, which contains several user-level device drivers as well as the user-level TZ VMM. The VMM is responsible for managing the normal world. In particular, it loads the image of the normal-world OS and triggers the switch to the normal world using a service provided by core. Each time, the normal world passes control to the secure world or attempts to perform an invalid operation, core reflects the resulting world switch to the VMM. So the VMM can process hypercalls or invoke an emulation function accordingly and explicitly yields control back to the normal world. For the demonstration scenario, the VMM provides a virtual framebuffer and a virtual touchscreen device to the normal world. To keep the complexity of the VMM low, the interactions of the normal world with these virtual devices are implemented as hypercalls (rather than faithful emulations of the complex i.MX hardware devices). The CSU is configured such that the Android OS is able to access the Graphics Processing Unit (GPU) directly. However, the GPU targets all rendering operation to the virtual framebuffer rather than the physical framebuffer as used by the IPU. This way, the VMM can deliberately direct the GPU output to a dedicated buffer, which is composed into the physical screen using a hardware overlay. Because the framebuffer driver is the only software component in control of the IPU, the display remains under the sole control of the secure world, yet there exists a direct data path of pixels of the normal world to the display. Consequently, the graphics performance of Android in the demo scenario is on par with the performance of Android natively executed on the same platform. User input is always received by the secure world via the touchscreen driver and the Nitpicker GUI server. Hence, the routing policy of user-input events is under control of the secure world at all times. Only if the TZ VMM has the current input focus, nitpicker will route input events to the VMM, which, in turn, translates those events to input events for the virtual touchscreen used by Android. The demonstration scenario is available at the following branch of Genode. https://github.com/skalk/genode/tree/i.MX53\_tablet\_demo Genode as secure OS on a i.MX53 SABRE tablet. Detailed instructions about reproducing it are provided by the README file at the os/src/server/vmm/imx53/ directory.

* * *

**ChatGPT:**

Title: TrustZone Demonstration Scenario on i.MX53 SABRE Tablet

Summary: The demonstration scenario for ARM TrustZone on i.MX53 SABRE tablet consists of key components like Genode's core, user-level device drivers, and a user-level TZ VMM, which manages the normal world. The VMM provides a virtual framebuffer and virtual touchscreen device to the normal world, with Android OS having direct access to the GPU. This setup maintains graphics performance and ensures the secure world retains control of the display and user input routing. The demonstration scenario can be accessed through the provided GitHub repository, with detailed instructions for reproducing it available in the README file.

* * *

**You:**

Common questions, answered In this Section, we attempt to answer common questions that we were repeatedly asked. Note that we are by no means experts in all areas covered. So if you detect errors, please report them back, preferably on our mailing list. What are the capabilities of TrustZone? TrustZone technology can be viewed from two angles, as virtualization solution and as mechanism to implement functionality similar to Trusted Platform Modules (TPM). When regarded as virtualization solution, TrustZone is severely lacking. The number of virtual machines is limited to two, one running in the secure world and one running in the non-secure world. There are no means for protecting multiple OSes sharing the non-secure world. There is no support to virtualize MMIO resources via the trap-and-execute model. As described in Section Device emulation, access violations of the non-secure OS can be detected but not emulated. Consequently, multiplexing a single device for both worlds is not possible in a transparent way. To guarantee that both worlds access distinct device resources only, certain device drivers of the non-secure OS must be modified. The use of TrustZone is not transparent. Even though those modifications are minor, this limitation effectively prevents the reuse of operating systems that are available as binaries only. There is no way to virtualize the physical memory as used by the non-secure OS. The guest-physical memory always corresponds to the host-physical memory. Despite those limitations, we identified a single advantage of TrustZone compared to other virtualization technologies (such as VT-x and recent ARM virtualization extensions), which is the direct assignment of device interrupts to the non-secure world without involving the VMM as indirection. We ultimately reached the conclusion that perceiving TrustZone as a virtualization mechanism is ill-guided. When looking at TrustZone as an alternative for TPMs, the motivation behind this technology become much more clear. In contrast to fixed-function TPMs, TrustZone is a vastly more versatile mechanism. The currently active world is represented by the so-called non-secure bit (NS bit) at the interconnect. The NS bit is routed to peripherals similar to an additional address line. This enables peripherals to respond to this condition by implementing restrictive policies for the NS mode. Thereby, security functions implemented in the secure world of TrustZone can utilize such peripherals. In contrast to TPMs, the security functions of the secure world of TrustZone are freely programmable using a powerful general-purpose CPU architecture. The port of the Genode OS Framework (as a poster child of a sophisticated component-based operating system) to the secure world is illustrative in this respect. In contrast, running Genode within a TPM would naturally be out of question. What are the limitations of TrustZone for compartmentalization? There are only two "worlds". Access by the non-secure side to the physical address space can be restricted but physical addresses are not virtualized. The granularity of access restricts depends on the SoC. For example, the Versatile Express platform provides no means to partition the DDR RAM into secure and non-secure areas. In contrast, the Freescale i.MX SoC provides this principal ability. The use of TrustZone is not entirely transparent to the non-secure side because non-accessible physical resources appear as holes in the physical address space. Furthermore, access to central devices (such as the system control registers) cannot be transparently emulated. The OS running on the non-secure world must be slightly modified. How to host two different compartments/zones (one trusted, one untrusted)? The general approach consists of the following steps: The system starts in secure mode and boots the hypervisor. The hypervisor sets up the non-secure world (i.e., by configuring the TZPC, TZASC, and PIC). The hypervisor loads the OS image to be executed in the non-secure world. The hypervisor enters the non-secure world at the entry point of the non-secure OS. The non-secure OS issues hypercalls for functions that are hidden from the non-secure world. Those hypercalls are handled by the hypervisor. In our particular experiments, the hypervisor is represented by an instance of the Genode OS, which separates the handling of hypercalls from the low-level mode switching using microkernel techniques. The individual steps of this process are covered in more detail in section Hypervisor managing the non-secure world.

* * *

**ChatGPT:**

Title: TrustZone Common Questions and Answers

Summary: TrustZone technology is best viewed as an alternative to TPMs rather than as a virtualization solution. It offers versatility and programmability, but it has limitations for compartmentalization, such as only having two worlds, non-virtualized physical addresses, and granularity of access restrictions that depend on the SoC. To host two different compartments or zones (trusted and untrusted), a hypervisor is utilized to set up the non-secure world, load the OS image for the non-secure world, and handle hypercalls from the non-secure OS. In experiments, the Genode OS was used as the hypervisor for this purpose.

* * *

**You:**

Does it make sense to run commodity OSes like Android in the secure world? Following the rationale of Section What are the capabilities of TrustZone?, the use of TrustZone is meaningful only for implementing security functions. Thereby, the complexity of implementation is crucial. Traditionally, the code executed in the secure world has library-like functionality. Running a complete OS such as Genode in the secure world yields more flexibility on the cost of added complexity. Running a monolithic OS on the secure world would increase the complexity in multiple orders of magnitude. On platforms such as the Versatile Express platform, only small portions of memory can be preserved to the secure world when also running a non-secure OS. I.e., the particular platform hosts 32 MiB of SRAM. This limitation naturally rules out complex operating systems such as Android. How does TrustZone compares to ARM's virtualization extensions? The virtualization extensions introduced with Cortex-A15 are orthogonal to TrustZone. There are no significant changes between the TrustZone implementations of Cortex-A9 and Cortex-A15. The virtualization extensions devise the implementation of the virtual machine monitor as part of the non-secure world. Those extensions are unavailable in the secure world (which is aligned with the idea of implementing mere TPM-like functionality in the secure world). Are there any security improvements of the Cortex-A15 over the A9 architecture then? The virtualization extensions introduced with Cortex-A15 offer an additional instrument for partitioning of the system through the "Hyp" (hypervisor) mode on the non-secure side. With this mode and the additional virtualization features, low-complexity virtual machine monitors become feasible. However, with regard to the protection of the secure world, there is no improvement over Cortex-A9. That said, the security properties of TrustZone largely depend on the SoC rather than the revision of the ARM CPU core. Cortex-A15-based SoCs may offer more flexibility with regard to the secure world (such as more peripherals responding to the NS bit). However, we have not thoroughly examined those SoC-vendor-specific implementations at large. What are the capabilities of ARM's virtualization extensions? There is a new CPU privilege level ("Hyp" mode) below the existing CPU modes, which is only supported in non-secure mode. Virtualization holes present in previous generations of the ARM architecture have been fixed for the Hyp mode. Consequently all privileged instructions trap into Hyp mode when executed in the other modes. Thereby, the architecture has become fully virtualizable by the means of the trap-and-execute model. The trap-and-execute model principally allows for executing unmodified guest OSes on top of the VMM. However, this model has inherent performance penalties when the guest OS performs privileged operations at a high rate, for example, when clearing interrupts at the interrupt controller. To mitigate those effects, hardware support for effectively avoiding the frequent intervention of the hypervisor has been introduced. In particular, the handling of virtual interrupts can be accelerated by using a new virtual IRQ controller (vIRQ) device. The hypervisor can present the vIRQ to the guest OS at the guest-physical location of the normal interrupt controller. Hence, the guest will always interact with the vIRQ device. When the guest OS clears an interrupt, the hypervisor does not get involved. However, the injection of interrupts into the virtual machine is exclusively done by the hypervisor. There is no way to directly assign device interrupts to virtual machines because the scheduling of (multiple) virtual machines on one CPU is implemented in the hypervisor. Hence, each device interrupt designated for a virtual machine will take the hop through the hypervisor. The Cortex-A15 facilitates the emulation of memory-mapped device registers by providing useful information to the virtual machine monitor. In addition to the program counter and fault address, the VMM receives the decoded instruction and the type of access. This alleviates the need of the VMM to access guest memory (to fetch the instruction) and simplifies the instruction decoding. To support multiple virtual machines, a guest-physical to host-physical address translation has been introduced, which is a mechanism similar to extended page tables (EPT) of VT-x. Thereby, guest-physical memory becomes fully virtualizable. This feature comes along with a new page-table format, which is optional for guest-virtual to guest-physical mappings and mandatory for guest-physical to host-physical mappings. Besides the support for guest-physical to host-physical mappings, the new format has the benefit of supporting more than 4 GiB of RAM in total (per VM, the amount of usable RAM is still restricted by 32-bit addressing). Thanks to tagged TLBs, there exists a fast path for the translation from guest-virtual to host-physical mappings. There is no virtualization of DMA accesses issued by bus peripherals (i.e., display controller uses host-physical addresses). If the guest OS contains a device driver, the guest has to use host-physical addresses to interact with the device. For example, addresses of DMA buffers supplied to a device cannot be specified as guest-physical addresses. Therefore, in the general case, DMA-using devices cannot be passed directly to a guest OS. Access to such devices must be intercepted by the hypervisor to translate those addresses. There is no DMA protection. Additional per-device MMUs would be required. The presence of such per-device MMUs depends on the SoC. IRQs designated to a device driver running in a guest OS are always handled by the hypervisor, which responds to the IRQ by injecting a virtual interrupt to the vIRQ device. Hence, each interrupt carries the overhead of switching the context between the Guest OS and the hypervisor. However, the relevance of this overhead in practice is uncertain. For more information on ARM virtualization extensions and the procedure of creating a Cortex-A15 based virtual machine monitor, let us refer you to the excellent document "Implementing Hardware-supported Virtualization in OKL4 on ARM" by Prashant Varanasi. How does TrustZone help to securely store secrets? Hiding peripherals and memory from the non-secure world is a key feature of TrustZone. TrustZone does not define, which peripherals and memory are subjected to this mechanism. This is in the hands of the SoC vendors. For example, SoCs of Freescale i.MX family come with RAM and ROM resources that are entirely located on chip. Hence, bus transactions concerning these resources are not visible at the wiring of the chip. By declaring those resources to be exclusively accessible by the secure world, the information stored and processed in these resources remain private to the secure software stack. That said, each SoC has different characteristics with regard to assigning or partitioning storage resources for the access of either world. Hence, there is no general answer to this question. How does TrustZone facilitate secure booting? As a precondition for the use of TrustZone for secure booting, the code running in the secure world must be bootstrapped in a secure way, which is SoC-specific. For example, the i.MX family provides a high-assurance boot (HAB) feature that could be used to securely bootstrap the secure world. Alternatively, the secure software could be fixed in a chip-internal flash or ROM at production time. For example, the popular range of low-cost ARM development boards such as Pandaboard come with a fixed ROM boot code that implements several hypercalls and switches to non-secure mode right before starting the u-boot boot loader. Because the internal ROM code cannot be bypassed, there is no way for any system booted on such devices to access device resources that are preserved to the secure world. Given that the secure world is booted in a secure fashion, the loader of the non-secure OS is in the position to validate the integrity of the boot image of the non-secure OS via cryptographic measures. In the case of Genode running in the secure world, such functionality could be implemented within the user-level VMM component. If the SoC lacks a way to fix the boot code for the secure world, secure booting cannot be implemented even if the platform is equipped with TrustZone technology. When using Genode as secure OS, the SoC should provide sufficient memory to be preserved for the secure world. Early platforms such as the Samsung S3C6410 that come with only a few KiB of secure RAM and ROM are ruled out.

* * *

**ChatGPT:**

Title: TrustZone and Commodity OSes, ARM's Virtualization Extensions, and Secure Booting

Summary: Running commodity OSes like Android in the secure world of TrustZone is not recommended due to increased complexity and limitations on platforms like the Versatile Express platform. ARM's virtualization extensions, introduced with Cortex-A15, are orthogonal to TrustZone and provide additional capabilities for partitioning systems through the Hyp mode. TrustZone can help securely store secrets by hiding peripherals and memory from the non-secure world and can facilitate secure booting if the SoC supports securely bootstrapping the secure world. The implementation of secure booting and secure storage depends on the SoC used.

* * *

**You:**

Please compare TrustZone and TPM in a table.

* * *

**ChatGPT:**

| Feature | TrustZone | TPM |
| --- | --- | --- |
| Purpose | Hardware-based security solution | Hardware-based security solution |
| Security functions | Freely programmable | Fixed-function |
| Execution environment | Secure world on ARM-based SoC | Standalone chip |
| Isolation | Two worlds: Secure and Non-secure | Separate from CPU |
| Complexity | Varies, from simple libraries to full OS | Limited, designed for specific functions |
| Interaction with peripherals | NS bit determines peripheral access control | Communicates via standard bus protocols |
| Cryptographic capabilities | Software implemented, based on user needs | Built-in cryptographic functions |
| Secure storage | Depends on SoC implementation | Built-in non-volatile storage |
| Secure boot | SoC-dependent, can be implemented | Provides support for secure boot process |
| Virtualization support | Limited, not designed for virtualization | Not applicable |
| Flexibility | More versatile, programmable functions | Less versatile, fixed-function |
| Performance impact | Depends on implementation complexity | Minimal, as it operates independently |

Please note that this comparison is a high-level overview of TrustZone and TPM. The specific features and capabilities may vary depending on the implementation and the SoC used for TrustZone or the TPM version and vendor.

* * *

**You:**

What is bootstrap code?

* * *

**ChatGPT:**

Bootstrap code, also known as boot code, bootloader, or bootstrapping, is a small program responsible for initializing a computer's hardware components and loading the operating system (OS) into memory. When a computer is powered on or restarted, the bootstrap code is the first code to execute, typically stored in a fixed location, such as a Read-Only Memory (ROM) chip, or firmware like Basic Input/Output System (BIOS) or Unified Extensible Firmware Interface (UEFI).

The primary function of the bootstrap code is to perform hardware checks, initialize essential hardware components (like CPU, memory, and peripherals), and locate the operating system's kernel. Once the kernel is found, the bootstrap code loads it into memory and transfers control to the kernel, enabling the OS to start and manage system resources.

In summary, bootstrap code is responsible for the initial steps in the boot process, laying the groundwork for the operating system to take over and provide a functional environment for the user.

* * *

**You:**

What are two lines?

* * *

**ChatGPT:**

The term "two lines" can refer to different things based on the context in which it is used. Here are a couple of interpretations:

1.  Geometry: In geometry, two lines refer to two straight, one-dimensional objects that extend infinitely in both directions. These lines can be parallel (never intersecting), intersecting (crossing at one

* * *

**You:**

What are two lines of experimentation? Please summarize them in short.

* * *

**ChatGPT:**

Two lines of experimentation refer to two distinct approaches or methods used to investigate a problem, hypothesis, or research question. In scientific research, these two lines can help validate results, uncover new insights, or compare different strategies. Here's a brief summary of each line:

1.  Line 1: This line of experimentation focuses on a particular method, technique, or approach to addressing the research question. It can involve specific experimental designs, data collection methods, or analysis techniques to investigate the hypothesis or problem.
    
2.  Line 2: This second line of experimentation employs an alternative method or approach to explore the same research question. By utilizing a different technique, researchers can compare the outcomes of both lines of experimentation and validate their findings or reveal new aspects of the research question that were not apparent in the first line of experimentation.

* * *

**You:**

What are two lines in the section "Starting point" in the article?

* * *

**ChatGPT:**

In the context of the "Starting point" section of the article, two lines refer to two distinct approaches to exploring TrustZone technology:

1.  Line 1: Utilize TrustZone as a virtualization solution, exploring its potential to host multiple virtual machines or support multiple operating systems in the secure and non-secure worlds. This line of experimentation seeks to understand TrustZone's capabilities as a virtualization mechanism.
    
2.  Line 2: Use TrustZone as an alternative to Trusted Platform Modules (TPM), focusing on its ability to implement security functions and protect sensitive information within the secure world. This line of experimentation aims to investigate the versatility and programmability of TrustZone as a security mechanism compared to fixed-function TPMs.

* * *

**You:**

Can Normal world and Secure World run at the same time in ARM?

* * *

**ChatGPT:**

In ARM TrustZone, the Normal world and Secure world cannot run concurrently. The processor can only execute code in either the Normal world or the Secure world at any given time. The two worlds are isolated from each other, and the processor switches between them based on events such as interrupts or requests for secure services. TrustZone uses a secure monitor mode to facilitate the transition between the two worlds, ensuring that the secure and non-secure states remain separate and protected.

* * *

**You:**

But can Normal world and Secure World run at the same time in multi processors of ARM?

* * *

**ChatGPT:**

Yes, in a multi-processor ARM system, it is possible for the Normal world and Secure world to run concurrently on separate cores. Each core in the system can be executing in either the Normal world or the Secure world independently. This allows for parallel processing of tasks in both worlds. However, it is important to note that the isolation between the two worlds is still maintained, and each core must follow the same TrustZone mechanisms to transition between the worlds when required.

* * *

**You:**

How to define memory size of secure world?

* * *

**ChatGPT:**

Defining the memory size for the secure world in an ARM TrustZone-enabled system is highly dependent on the specific System-on-Chip (SoC) being used. Each SoC has different characteristics and mechanisms for allocating and partitioning memory resources between the secure and non-secure worlds.

Typically, the memory size for the secure world is defined during the system's initialization or configuration phase. The process involves configuring TrustZone-specific hardware components such as TrustZone Protection Controller (TZPC) and TrustZone Address Space Controller (TZASC) to set access permissions and memory partitions.

To define the memory size of the secure world, follow these general steps:

1.  Determine the available memory resources: Consult your SoC's technical reference manual or datasheet to identify the available memory resources and their respective addresses.
    
2.  Configure TZPC and TZASC: Based on the desired memory size for the secure world, configure the TZPC and TZASC registers to partition the memory accordingly. This may involve setting up specific regions and access permissions for secure and non-secure worlds. Some SoCs might provide alternative or additional mechanisms for memory partitioning.
    
3.  Verify and update your secure world software: Ensure your secure world software is aware of the allocated memory size and adapts its memory management accordingly.
    

Please note that these steps are generalized, and you should refer to the documentation of your specific SoC for exact procedures and register configurations.

* * *

**You:**

Can memory size of secure world be changed?

* * *

**ChatGPT:**

In most ARM TrustZone-enabled systems, the memory size of the secure world is typically defined during the system's initialization or configuration phase. However, whether the memory size of the secure world can be changed at runtime depends on the specific System-on-Chip (SoC) being used and its support for dynamic memory partitioning.

Some SoCs may allow for dynamic reconfiguration of TrustZone components like the TrustZone Protection Controller (TZPC) and TrustZone Address Space Controller (TZASC) during runtime, enabling changes to memory partitioning between the secure and non-secure worlds. In such cases, the secure world software would also need to support and be aware of such changes to adapt its memory management accordingly.

To determine if your specific SoC supports changing the memory size of the secure world at runtime, consult the technical reference manual or datasheet provided by the manufacturer. It's important to consider the potential security implications and any restrictions when dynamically changing memory partitioning, as it could introduce new attack surfaces or vulnerabilities.

* * *

**You:**

What is SMC?

* * *

**ChatGPT:**

SMC stands for Secure Monitor Call, which is an ARM instruction used in TrustZone-enabled systems. The SMC instruction is used to transfer control between the non-secure (Normal) world and the secure world. When the non-secure world needs to access a secure resource or service, it uses the SMC instruction to trigger a switch to the secure world. The secure world then handles the request, performs the necessary operations, and returns control back to the non-secure world using the ERET (Exception Return) instruction.

The SMC instruction ensures that transitions between the two worlds are securely managed and controlled, allowing the secure world to maintain its isolation and integrity. Secure Monitor Calls are essential for implementing security services and trusted applications that require isolation from the non-secure world while still providing a controlled interface for communication between the two worlds.

* * *

**You:**

Can secure world request a service in normal world via SMC?

* * *

**ChatGPT:**

Yes, the secure world can request a service in the normal world via SMC. Although it's more common for the normal world to request services from the secure world, the secure world may still need to access certain resources or services in the normal world. In such cases, the secure world can use SMC to make a request to the normal world.

However, it's important to note that the secure world should carefully manage any interactions with the normal world to avoid compromising its own security. When the secure world needs to access services or resources in the normal world, it should do so with the understanding that the normal world is potentially untrusted and might attempt to exploit any vulnerabilities in the communication process. Therefore, the implementation of such communication should be done cautiously, with a focus on maintaining the isolation and integrity of the secure world.

* * *

**You:**

What is SPD?

* * *

**ChatGPT:**

In the context of ARM TrustZone, SPD (Secure Payload Dispatcher) is a component responsible for managing and dispatching Secure Partition (SP) requests. An SPD serves as an intermediary layer between the normal world and secure world, allowing for the secure processing of service requests from the normal world.

When a normal world application requires services provided by the secure world, it issues a request via SMC (Secure Monitor Call). The SPD receives this request, identifies the appropriate secure partition to handle the request, and dispatches the service execution to the corresponding partition. After the secure partition has processed the request, the SPD returns the result to the normal world.

By using an SPD, the secure world can maintain better isolation and security, as the SPD ensures that the normal world does not have direct access to secure partitions or their resources.

* * *

**You:**

Can SPD handle the request from the secure world?

* * *

**ChatGPT:**

Yes, the Secure Payload Dispatcher (SPD) can handle requests from both the normal world and the secure world. Although it is more common for the normal world to make service requests to the secure world, there might be cases where the secure world needs to access resources or services available in the normal world.

In such scenarios, the SPD plays a similar role in managing and dispatching these requests. It serves as an intermediary between the two worlds, ensuring that the communication is secure and that the appropriate services are invoked to handle the requests. This way, the secure world can access resources in the normal world without compromising its security and isolation.

* * *

**You:**

What is SP?

* * *

**ChatGPT:**

SP stands for Secure Partition, which is a software component or execution environment running within the secure world of ARM TrustZone. Secure Partitions are designed to provide isolation and protection for sensitive code and data, such as cryptographic operations, key management, or secure storage. The secure world hosts these SPs, which can communicate with the normal world through a well-defined interface, typically via SMC (Secure Monitor Call) instructions.

SPs help to ensure that critical operations and information remain protected from potentially malicious or insecure code running in the normal world. By isolating these components, TrustZone enhances the overall security of a system.

* * *

**You:**

Can different SPs communicate together?

* * *

**ChatGPT:**

Yes, different Secure Partitions (SPs) can communicate with each other within the secure world. However, this communication should be carefully designed and managed to maintain the isolation and security properties of each SP. Typically, an intermediary component like a secure partition manager or the secure monitor itself is responsible for facilitating communication between different SPs, ensuring that information sharing adheres to the security policies and requirements of each partition.

To enable secure communication between different SPs, developers should implement well-defined interfaces and access control policies to prevent unauthorized access or information leaks between partitions, maintaining the overall security goals of the system.

* * *

**You:**

What is SPM?

* * *

**ChatGPT:**

SPM stands for Secure Partition Manager. In the context of ARM TrustZone or systems with secure partitions, the SPM is a component responsible for managing and orchestrating the execution of Secure Partitions (SPs). The SPM's role includes controlling access to resources, managing communication between SPs, ensuring the isolation of different secure partitions, and enforcing security policies.

In a nutshell, the Secure Partition Manager provides a framework for the secure world to manage the lifecycle and interactions of multiple secure partitions, ensuring that the security and isolation properties of each partition are maintained.

* * *

**You:**

How to create a SP and when?

* * *

**ChatGPT:**

Creating a Secure Partition (SP) typically involves a few steps and is usually done during the system initialization or when a secure application needs to be launched. Here are the steps to create an SP:

1.  Design: Begin by identifying the secure functionality or application you want to isolate in a separate SP. Determine the security requirements, resource access, and communication interfaces needed for the secure partition.
    
2.  Implementation: Implement the secure functionality or application, adhering to the security requirements and following best practices for secure programming. This may involve writing code and creating any necessary data structures, as well as implementing communication interfaces to interact with other SPs or the normal world.
    
3.  Configuration: Configure the system to support the SP. This might involve configuring memory regions, peripherals, and access controls to meet the security requirements of the SP. This is typically done in the system's bootloader, firmware, or Secure Partition Manager (SPM), depending on the platform.
    
4.  Initialization: Load and initialize the SP during system startup or when required. This process includes loading the secure partition's code and data into the protected memory regions and initializing the partition's state. The SPM or another trusted component may handle this initialization process.
    
5.  Execution: Once initialized, the SP can be executed, providing its secure functionality to other components or applications in the system. The SPM or a trusted scheduler will manage the execution of the SP, ensuring proper isolation and adherence to security policies.
    

Creating an SP depends on the specific platform or system you are working with, as well as the requirements of your secure application. Ensure that you consult the relevant documentation and guidelines for your platform to create and manage secure partitions effectively.

* * *

**You:**

Can I create a SP in run-time?

* * *

**ChatGPT:**

Creating a Secure Partition (SP) during runtime is generally not recommended, as it could introduce security risks and may not be supported by some platforms. Secure Partitions are typically initialized during system startup or secure application launch to ensure proper isolation and security.

However, if your platform supports creating an SP during runtime and you have a valid use case, it might be possible. You would need to ensure that you take the necessary precautions to maintain the security of the system and the SPs, including:

1.  Ensuring proper isolation between the newly created SP and the rest of the system, including other SPs.
2.  Configuring memory regions, peripherals, and access controls correctly.
3.  Verifying the integrity and authenticity of the code and data being loaded into the new SP.

Keep in mind that creating an SP during runtime may be more complex and error-prone than creating one during system startup or secure application launch. You should carefully consider the security implications and consult your platform's documentation to determine if this approach is supported and appropriate for your use case.

* * *

**You:**

What is TA?

* * *

**ChatGPT:**

TA stands for Trusted Application. In the context of ARM TrustZone or Trusted Execution Environments (TEEs), a Trusted Application is a secure piece of software running in the secure world. These applications are designed to handle sensitive data or perform security-critical operations, isolated from the normal world or non-secure applications.

Trusted Applications typically run on top of a TEE Operating System (TEE OS), which provides services like secure storage, cryptographic operations, and secure communication with the normal world. The TEE OS is responsible for managing and isolating multiple Trusted Applications, ensuring that they don't interfere with each other or leak sensitive data. Examples of TEE OSs include OP-TEE and Trustonic Kinibi.

Trusted Applications are usually loaded and instantiated by the TEE OS based on requests from the normal world or other secure world components. They can be used to perform a wide range of tasks, such as digital rights management, secure payment processing, biometric authentication, and more.

* * *

**You:**

What are relationships between TA and SP?

* * *

**ChatGPT:**

Trusted Applications (TAs) and Secure Partitions (SPs) are related concepts in the context of ARM TrustZone and secure computing, but they are not the same. Both are mechanisms for running secure code within a Trusted Execution Environment (TEE) to handle sensitive data and perform security-critical operations, isolated from the normal world. However, they differ in their design, implementation, and use cases.

Trusted Applications (TAs):

1.  TAs are secure software components running on a TEE Operating System (TEE OS) like OP-TEE or Trustonic Kinibi.
2.  The TEE OS manages the TAs, providing isolation between them and offering secure services such as cryptographic operations, secure storage, and communication with the normal world.
3.  TAs are typically used for specific security functions or operations like digital rights management, secure payment processing, biometric authentication, and more.

Secure Partitions (SPs):

1.  SPs are part of the ARMv8.4-A architecture, which introduces the concept of ARM Confidential Compute Architecture (CCA).
2.  SPs provide a way to partition and isolate secure software components directly at the hardware level, without the need for a TEE OS.
3.  Each SP runs in its own isolated environment, with dedicated memory and resources, and can communicate with other SPs or the normal world using a defined protocol.

In summary, while both TAs and SPs serve the purpose of providing secure environments for handling sensitive data and operations, TAs rely on a TEE OS to manage them and provide services, while SPs are isolated directly at the hardware level without the need for a TEE OS. SPs are a newer concept introduced with ARMv8.4-A architecture, whereas TAs have been used in earlier versions of ARM TrustZone.

* * *

**You:**

Can I say that an SP contain many TAs?

* * *

**ChatGPT:**

It would not be accurate to say that an SP contains many TAs because they are separate concepts with different implementations and use cases. TAs are secure software components running on a TEE OS like OP-TEE or Trustonic Kinibi, while SPs are part of the ARMv8.4-A architecture and do not rely on a TEE OS. SPs provide isolation and secure execution directly at the hardware level.

You can think of TAs as a way to implement secure functions within a TEE OS, while SPs provide a mechanism to create isolated execution environments at the hardware level without depending on a TEE OS. They both serve the purpose of providing secure environments for handling sensitive data and operations but do so in different ways. Therefore, it would be more appropriate to view TAs and SPs as distinct, independent entities rather than one containing the other.

* * *

**You:**

Can I say that a TA uses a SP?

* * *

**ChatGPT:**

No, it would not be accurate to say that a TA uses a SP, as they are separate concepts with different implementations and use cases. TAs (Trusted Applications) are secure software components running within a TEE OS like OP-TEE or Trustonic Kinibi, while SPs (Secure Partitions) are part of the ARMv8.4-A architecture and do not rely on a TEE OS. SPs provide isolation and secure execution directly at the hardware level.

TA and SP both serve the purpose of providing secure environments for handling sensitive data and operations, but they do so in different ways and are not directly related. TAs operate within the context of a TEE OS, whereas SPs provide isolation at the hardware level, independent of any specific TEE OS.

* * *

**You:**

How does TA use SP?

* * *

**ChatGPT:**

TA (Trusted Application) and SP (Secure Partition) are separate concepts and are not meant to be used together directly. TA is a software component that runs within a Trusted Execution Environment (TEE) OS, such as OP-TEE or Trustonic Kinibi. On the other hand, SPs are introduced in the ARMv8.4-A architecture and provide isolation and secure execution at the hardware level, without relying on a TEE OS.

In a system that utilizes both TAs and SPs, a TA would not directly use an SP. Instead, the TA would interact with the TEE OS or other components within the secure world to perform its functions. The SP would provide isolation and security at the hardware level, independently of the TAs and the TEE OS.

In summary, TAs and SPs are separate entities with different implementations and use cases. They both contribute to creating secure environments for sensitive data and operations, but they do not have a direct relationship where a TA would use an SP.

* * *

**You:**

How do I leverage TAs and SPs?

* * *

**ChatGPT:**

To leverage TAs (Trusted Applications) and SPs (Secure Partitions) effectively, you need to follow these steps:

1.  Understand the target platform: Determine if the target platform supports a Trusted Execution Environment (TEE) OS for TAs or ARMv8.4-A architecture for SPs. Choose the appropriate technology based on the platform's support and your security requirements.
    
2.  Implement Trusted Applications (TAs): a. Choose a TEE OS: Select a TEE OS, such as OP-TEE, Trustonic Kinibi, or another TEE OS compatible with your platform. b. Develop TAs: Write the TAs that perform security-sensitive operations or handle sensitive data. TAs run within the TEE OS, providing a secure and isolated environment. c. Deploy TAs: Package and deploy TAs to the target platform according to the TEE OS's requirements and guidelines.
    
3.  Implement Secure Partitions (SPs): a. Set up the environment: Ensure your platform and development tools support the ARMv8.4-A architecture with the required security extensions. b. Develop SPs: Write the SPs that perform security-sensitive operations or handle sensitive data. SPs provide hardware-level isolation and security, without relying on a TEE OS. c. Configure resources: Define the resources, such as memory regions and peripherals, accessible by each SP. Set access permissions and isolation levels according to your security requirements. d. Deploy SPs: Package and deploy the SPs to the target platform according to the ARMv8.4-A architecture requirements and guidelines.
    
4.  Secure communication: Establish secure communication channels between the normal world and the secure world, which may involve TAs and SPs. Use mechanisms such as remote procedure calls (RPCs) or SMC (Secure Monitor Calls) to facilitate communication.
    
5.  Integrate with the normal world: Develop applications and services in the normal world that interact with TAs and SPs for security-sensitive operations. Ensure the normal world applications and services adhere to best practices for security, such as proper authentication and access control.
    

By following these steps, you can effectively leverage TAs and SPs to create a secure environment for sensitive data and operations on your ARM-based platform.

* * *

**You:**

How do TAs and SPs communicate each other?

* * *

**ChatGPT:**

TAs (Trusted Applications) and SPs (Secure Partitions) can communicate with each other using Inter-Partition Communication (IPC) mechanisms, which are platform-specific and depend on the underlying TEE (Trusted Execution Environment) OS or ARMv8.4-A architecture implementation.

When TAs and SPs need to communicate, they typically follow these steps:

1.  Establish a communication channel: Both TAs and SPs should have a well-defined communication interface, such as shared memory or message passing. The implementation details depend on the TEE OS for TAs and the platform's support for SPs.
    
2.  Secure the communication channel: To ensure the confidentiality and integrity of data exchanged between TAs and SPs, use cryptographic techniques, such as encryption and authentication.
    
3.  Exchange messages: TAs and SPs can exchange messages through the established communication channel. These messages may include requests for services, data to be processed, or responses.
    
4.  Synchronize communication: Depending on the IPC mechanism used, it may be necessary to implement synchronization primitives, such as semaphores or mutexes, to coordinate communication between TAs and SPs.
    
5.  Handle errors and exceptions: Implement error handling and exception mechanisms to manage communication failures, timeouts, or other unexpected events.
    

It is essential to note that the communication between TAs and SPs requires careful implementation to ensure security and prevent potential attacks. Therefore, following best practices and guidelines for secure IPC is critical when developing communication between TAs and SPs.

* * *

**You:**

Why are SPD and SPM mutually exclusive?

* * *

**ChatGPT:**

The Secure Partition Manager (SPM) and the Secure Partition Dispatcher (SPD) are two different approaches to managing secure partitions in the ARMv8.4-A architecture, and they are mutually exclusive because they serve different purposes and are intended for different use cases.

1.  Secure Partition Manager (SPM): SPM is designed for the ARMv8.4-A architecture and is responsible for managing Secure Partitions (SPs). SPs are isolated execution environments running inside the secure world, which can host multiple security services or Trusted Applications (TAs). The SPM is responsible for creating, initializing, scheduling, and managing communication between SPs. It enables fine-grained partitioning of resources and services within the secure world.
    
2.  Secure Partition Dispatcher (SPD): SPD is a part of ARM Trusted Firmware (ATF) and is used to manage secure services in ARMv8-A architecture. SPD provides an interface between the Normal World (NW) and the Secure World (SW). It is responsible for dispatching secure service requests from the NW to the appropriate secure execution environment, such as an SP or a TA, and returning the results back to the NW.
    

The reason they are mutually exclusive is that they cater to different architectural versions and use cases. SPM is designed specifically for ARMv8.4-A and provides advanced features for managing SPs, while SPD is used in ARMv8-A to manage secure services.

Using both SPM and SPD simultaneously would lead to conflicts in terms of resource allocation, scheduling, and communication between the secure world and the normal world. To avoid confusion and ensure proper secure partition management, either SPM or SPD is used, depending on the target ARM architecture and the specific use case.

* * *

**You:**

Can a SP host many TAs?

* * *

**ChatGPT:**

A Secure Partition (SP) can host multiple Trusted Applications (TAs) in a single isolated execution environment within the secure world. The Secure Partition Manager (SPM) is responsible for managing and scheduling these TAs. Each TA can provide a specific security service, and they can all run within the same SP. By hosting multiple TAs within an SP, you can share resources among TAs, such as memory or peripherals, which can improve overall efficiency and reduce the overhead of managing individual TAs in separate SPs.

* * *

**You:**

Can a TA communicate different SP?

* * *

**ChatGPT:**

A Trusted Application (TA) can communicate with different Secure Partitions (SPs) through a secure communication channel, which is typically established by the Secure Partition Manager (SPM) or another trusted component in the secure world. The communication between TAs and different SPs is usually facilitated by a well-defined interface using messages or function calls. This allows TAs to request services or share data with other SPs in a controlled and secure manner, without directly accessing each other's memory or resources. However, it is important to note that the level of isolation between TAs and SPs may vary depending on the specific implementation and platform.

* * *

**You:**

What are EL0, EL1, EL2, S-EL0, S-EL1, S-EL2, S-EL3?

* * *

**ChatGPT:**

In the ARMv8-A architecture, the privilege levels (EL) define different modes of operation for the processor, with each level having different access rights and capabilities. There are four Exception Levels (EL0, EL1, EL2, and EL3), and each level can operate in both Secure and Non-Secure states. Here's a brief explanation of each:

1.  EL0: This is the least privileged level, where user-space applications run. It has limited access to system resources and cannot execute privileged instructions.
    
2.  EL1: This level is where the operating system kernel runs. It has more privileges than EL0, enabling it to manage system resources, configure the hardware, and isolate user-space applications from each other.
    
3.  EL2: This level is intended for hypervisors, which manage multiple virtual machines or operating systems. It provides the necessary isolation and control to manage virtualization.
    
4.  EL3: This is the most privileged level, typically used for low-level firmware, such as a bootloader or a Trusted Execution Environment (TEE). It is responsible for setting up the system and ensuring a secure boot process.
    

The "S-" prefix indicates that the exception level is operating in the Secure state, which is part of ARM's TrustZone technology. TrustZone creates a separate, isolated environment for secure applications and data, ensuring that sensitive information remains protected from potential attacks or unauthorized access:

1.  S-EL0: Secure User mode, where secure user-space applications run.
2.  S-EL1: Secure Kernel mode, where the secure operating system kernel runs.
3.  S-EL2: Secure Hypervisor mode, where a secure hypervisor can manage secure virtual machines.
4.  S-EL3: Secure Monitor mode, where low-level firmware like a secure bootloader or a TEE operates.

In summary, the ARMv8-A architecture organizes the privilege levels (EL0, EL1, EL2, and EL3) and the Secure (S-EL0, S-EL1, S-EL2, and S-EL3) and Non-Secure states to create a robust and flexible environment for running a mix of secure and non-secure applications, operating systems, and hypervisors.

* * *

**You:**

What are relationships of SPD, SPM and SMC?

* * *

**ChatGPT:**

The Secure Partition Manager (SPM), Secure Partition Dispatcher (SPD), and Secure Monitor Call (SMC) are related concepts in the context of ARM TrustZone technology, which provides a secure and isolated environment for sensitive applications and data. Here's a brief explanation of each concept and their relationships:

1.  Secure Monitor Call (SMC): SMC is a special instruction used to switch between the Secure and Non-Secure states in ARM TrustZone. When SMC is executed, the processor transitions to the Secure state, and the Secure Monitor (typically running at S-EL3) is responsible for handling the call. The Secure Monitor can then perform the requested operation or forward the request to a more specific component, such as the SPM or an SPD.
    
2.  Secure Partition Manager (SPM): The SPM is responsible for managing Secure Partitions (SPs), which are isolated execution environments that host Trusted Applications (TAs) or other secure services. The SPM handles tasks such as creating, initializing, and terminating SPs, as well as managing access to secure resources. When the Non-Secure world needs to access a service provided by an SP, it can use the SMC instruction to request the SPM's assistance.
    
3.  Secure Partition Dispatcher (SPD): The SPD is an optional component that facilitates communication between the Non-Secure world and the Secure world, particularly when using an SMC. The SPD can handle requests from the Non-Secure world, forward them to the appropriate SP, and return the results to the Non-Secure caller. In some implementations, the SPM and SPD can be combined into a single component.
    

In summary, SMC is an instruction used to transition between Secure and Non-Secure states, while the SPM and SPD are components that manage Secure Partitions and facilitate communication between the two worlds. When an SMC is issued, the request is

* * *

**You:**

What is Secure Monitor?

* * *

**ChatGPT:**

The Secure Monitor is a critical component of the ARM TrustZone security technology that acts as an intermediary between the Secure and Non-Secure worlds. It operates at the highest privilege level (S-EL3) within the Secure world, ensuring the integrity and confidentiality of the Secure environment.

The primary responsibilities of the Secure Monitor include:

1.  Handling transitions between Secure and Non-Secure states: When a Secure Monitor Call (SMC) instruction is executed by the Non-Secure world, the processor switches to the Secure state, and the Secure Monitor takes control to process the request. It can either perform the requested operation or forward the request to other components, such as the Secure Partition Manager (SPM) or a specific Secure Partition (SP).
    
2.  Managing resources and access control: The Secure Monitor oversees access to secure system resources, such as memory regions, peripherals, and cryptographic keys, ensuring that only authorized Secure software components can access them.
    
3.  Enforcing the security policy: The Secure Monitor is responsible for implementing and enforcing the overall security policy for the system. This includes defining the security boundaries between the Secure and Non-Secure worlds, as well as ensuring that the Secure world remains protected from potential attacks originating from the Non-Secure world.
    

In essence, the Secure Monitor is a vital component of ARM TrustZone that provides a trusted execution environment for security-sensitive applications and data, while also managing the transitions and interactions between the Secure and Non-Secure worlds.

* * *

**You:**

Is SPD an optional component?

* * *

**ChatGPT:**

Yes, the Secure Partition Dispatcher (SPD) is an optional component within the ARM TrustZone security architecture. The SPD is responsible for managing and scheduling the execution of Secure Partitions (SPs) in the Secure world. It is a more advanced way of handling Secure services compared to the traditional monolithic Secure Monitor, which directly handles Secure world requests.

Using SPD allows for a more modular and flexible approach to implementing Secure services. However, if your use case does not require the functionality provided by Secure Partitions, you can choose not to include the SPD in your system. In that case, you will rely on the Secure Monitor to handle Secure world requests directly or use a different mechanism for managing Secure services.

Ultimately, the choice of whether to include an SPD in your system depends on your specific security requirements and the desired level of flexibility and modularity in your Secure software stack.

* * *

**You:**

Can I use SPD instead of SM?

* * *

**ChatGPT:**

Yes, you can use the Secure Partition Dispatcher (SPD) instead of the traditional Secure Monitor (SM) in your ARM TrustZone-enabled system. The SPD provides a more flexible and modular approach to managing Secure services by handling and scheduling the execution of Secure Partitions (SPs) in the Secure world.

When using the SPD, the responsibility for managing Secure services is shifted from the monolithic Secure Monitor to the individual Secure Partitions, which are isolated from each other and can be developed and updated independently.

However, keep in mind that this decision depends on your specific security requirements and the desired level of flexibility and modularity in your Secure software stack. If you choose to use the SPD, it will replace the SM as the primary mechanism for managing Secure services in your system.

* * *

**You:**

Is normal world a secure parition?

* * *

**ChatGPT:**

No, the Normal World is not a Secure Partition. The Normal World and Secure World are separate execution environments in ARM TrustZone-enabled systems. The Secure World is designed for running security-sensitive code and handling sensitive data, whereas the Normal World is intended for running general-purpose applications and operating systems.

Secure Partitions (SPs) are isolated execution environments within the Secure World. These partitions allow the development and management of security services and Trusted Applications (TAs) independently from each other. They provide additional separation and isolation for sensitive code and data within the Secure World.

In contrast, the Normal World does not provide the same level of protection and isolation as the Secure World and its Secure Partitions, making it unsuitable for hosting security-critical components.

* * *

**You:**

Is secure world a secure partition?

* * *

**ChatGPT:**

No, the Secure World is not a Secure Partition, but it contains Secure Partitions. The Secure World is a separate, protected execution environment enabled by ARM TrustZone technology, designed for running security-sensitive code and handling sensitive data.

Secure Partitions (SPs) are isolated execution environments within the Secure World. They provide additional separation and isolation for sensitive code and data, allowing the development and management of security services and Trusted Applications (TAs) independently from each other.

So, while the Secure World provides a protected environment, Secure Partitions offer even more granular isolation within the Secure World itself.

* * *

**You:**

Does boot loader only run in secure world, not in normal world?

* * *

**ChatGPT:**

Bootloaders can run in both the Secure World and the Normal World, depending on the specific use case and platform. In a secure boot process, the initial bootloader stages run in the Secure World to ensure the integrity and authenticity of the system's firmware and subsequent software components.

Once the initial validation is complete, the bootloader may hand over control to the Normal World, allowing the operating system and applications to boot up and run.

However, in some cases, a bootloader may run entirely in the Normal World if the platform doesn't require secure boot or if the secure boot process is handled differently. Ultimately, whether the bootloader runs in the Secure World or the Normal World depends on the specific hardware, firmware, and security requirements of the system.

* * *

**You:**

How to swtich secure world to normal world when booting?

* * *

**ChatGPT:**

When booting a system with TrustZone technology, the processor starts in the Secure World by default. To switch from the Secure World to the Normal World during the boot process, you can follow these general steps:

1.  **Initialize the Secure World**: In the Secure World, the secure bootloader initializes the necessary hardware components, sets up the secure environment, and configures the memory and peripherals access permissions.
    
2.  **Validate and load the Normal World software**: The secure bootloader validates the Normal World software, such as the operating system or bootloader, using cryptographic techniques like digital signatures. Once validation is successful, it loads the software into the memory designated for the Normal World.
    
3.  **Configure the processor**: Before switching to the Normal World, the secure bootloader sets up the processor's state, registers, and exception levels. It also configures the system registers, such as the Secure Configuration Register (SCR) and the Monitor Vector Base Address Register (MVBAR), to define the behavior of the system when switching between the Secure World and the Normal World.
    
4.  **Switch to the Normal World**: The secure bootloader performs a Secure Monitor Call (SMC) or an Exception Return (ERET) to switch the processor from the Secure World to the Normal World. This transition is facilitated by the Secure Monitor, which is responsible for handling the state switch between the two worlds.
    

After these steps, the processor enters the Normal World, and the Normal World software, such as the operating system or bootloader, starts executing.

Please note that these steps are a general outline and may vary depending on the specific platform, hardware, and firmware implementations.

* * *

**You:**

Is TrustZone a software or hardware?

* * *

**ChatGPT:**

TrustZone is a hardware-based security technology implemented in ARM processors. It provides a security extension that enables the creation of a secure environment alongside the normal environment, isolating the execution of sensitive code and data from potential threats in the normal environment. TrustZone itself is not a software; however, it requires software support to fully utilize its features, such as secure operating systems, trusted applications, and secure bootloaders.

* * *

**You:**

Can TrustZone replace HSM?

* * *

**ChatGPT:**

TrustZone and Hardware Security Modules (HSMs) serve different purposes and have different characteristics. While TrustZone can provide a secure environment for sensitive code execution and data storage, it may not be a direct replacement for HSMs in all use cases.

HSMs are dedicated hardware devices designed to provide robust security for cryptographic operations and key management. They are typically certified to high security standards (such as FIPS 140-2 or Common Criteria) and are resistant to various physical and logical attacks.

TrustZone, on the other hand, is a security extension integrated into ARM processors, which aims to provide a secure environment within the same processor. It is not a separate dedicated hardware device like an HSM. TrustZone can offer a reasonable level of security but may not provide the same level of robustness or certification as an HSM.

In some use cases, TrustZone can be used as a lightweight alternative to an HSM, especially when cost, power consumption, and space are critical factors. However, for applications that require the highest levels of security and assurance, an HSM may still be the preferred choice.

Ultimately, whether TrustZone can replace an HSM depends on the specific security requirements and constraints of the system being designed.

* * *

**You:**

What is ATF?

* * *

**ChatGPT:**

ATF stands for ARM Trusted Firmware, which is an open-source project that provides a reference implementation of secure software for ARMv8-A-based platforms. The ARM Trusted Firmware provides a set of software components that are required to implement security features on ARMv8-A processors, such as those that support ARM TrustZone technology.

The main components of ARM Trusted Firmware include:

1.  BL1 (Boot Loader 1): The initial boot loader responsible for setting up a secure execution environment and loading the next stage of the boot process, usually BL2 or BL31.
    
2.  BL2 (Boot Loader 2): Responsible for loading and authenticating the remaining firmware images, such as BL31, BL32, and BL33. It typically performs additional platform-specific initialization and sets up memory partitioning.
    
3.  BL31 (EL3 Runtime Software): The runtime firmware that runs at Exception Level 3 (EL3) and provides services for managing the system power state, system resets, and the handling of SMC (Secure Monitor Call) between the secure and non-secure worlds.
    
4.  BL32 (Secure-EL1 Payload): Optional firmware that provides services to the secure world, such as a Secure Partition Manager (SPM) or a Trusted Execution Environment (TEE) like OP-TEE.
    
5.  BL33 (Non-secure world bootloader): The bootloader for the non-secure world, typically a bootloader like U-Boot or an operating system like Linux.
    

The ARM Trusted Firmware provides a foundation for developing secure software on ARM-based platforms and serves as a reference implementation for platform vendors and developers to build upon or customize for their specific needs.

* * *

**You:**

What is MMU?

* * *

**ChatGPT:**

MMU stands for Memory Management Unit. It is a hardware component found in many computer systems, including those based on the ARM architecture. The primary function of the MMU is to manage the system's memory by translating virtual memory addresses to physical memory addresses, enabling memory protection, and controlling access permissions for different regions of memory.

Key functions of an MMU include:

1.  Virtual-to-physical address translation: MMUs use a system of page tables to translate virtual memory addresses, used by software, to physical memory addresses, which correspond to the actual location of data in the memory hardware. This allows software to access memory in a uniform and consistent manner, even when the actual memory layout is fragmented or changes dynamically.
    
2.  Memory protection: MMUs enable separation and isolation of different memory regions based on the access permissions set for each region. This helps prevent unauthorized access to memory and protects the system from bugs, crashes, or security vulnerabilities that could result from unintended memory access.
    
3.  Caching and cache management: MMUs often work closely with the CPU's cache to ensure efficient and consistent access to memory. By managing cache attributes and maintaining a consistent view of memory, MMUs help improve overall system performance.
    
4.  Supporting virtual memory: MMUs play a crucial role in implementing virtual memory, which allows multiple applications and processes to run simultaneously while maintaining the illusion that each has access to a large, contiguous block of memory. Virtual memory allows the system to use disk space as an extension of RAM, effectively increasing the available memory and enabling better multitasking and memory management.
    

Overall, the MMU is an essential component in modern computer systems that helps manage memory efficiently, enhances system performance, and provides a foundation for implementing advanced memory-related features such as virtual memory and memory protection.

* * *

**You:**

What is TLB?

* * *

**ChatGPT:**

TLB stands for Translation Lookaside Buffer. It is a specialized cache used by a computer's memory management unit (MMU) to speed up the translation of virtual memory addresses to physical memory addresses. The TLB stores a small number of recently-used virtual-to-physical address mappings, allowing the MMU to quickly look up the physical address for a given virtual address without having to consult the full page table stored in main memory.

Since accessing the main memory is generally slower than accessing the cache, the TLB helps improve the overall performance of the system. When the MMU receives a virtual address to translate, it first checks the TLB to see if the required mapping is already present. If the mapping is found in the TLB (a TLB hit), the MMU can quickly obtain the corresponding physical address. If the mapping is not in the TLB (a TLB miss), the MMU must access the page table in main memory, which takes more time.

To maintain the efficiency of the TLB, the system uses various algorithms to decide which mappings should be stored in the TLB and which ones should be evicted when the TLB becomes full. These algorithms aim to optimize the TLB hit rate by keeping the most frequently or recently used mappings in the buffer.

In summary, the TLB is a critical hardware component that works with the MMU to accelerate virtual-to-physical address translation, thus improving overall system performance and reducing memory access latency.

* * *

**You:**

What is SMP?

* * *

**ChatGPT:**

SMP stands for Symmetric Multiprocessing. It is an architecture used in multi-core and multi-processor computer systems where two or more identical processors or processor cores are connected to a single shared memory and are controlled by a single operating system. In an SMP system, each processor or core can execute different tasks independently, but they share the same memory resources and I/O devices.

SMP allows for more efficient processing and better utilization of system resources, as multiple processors or cores can work simultaneously on different tasks, improving overall system performance. This architecture also provides better fault tolerance and load balancing, as tasks can be distributed among the available processors, reducing the workload on any single processor and minimizing the impact of a processor failure on the overall system.

In an SMP system, the operating system and applications must be designed to take advantage of multiple processors, using techniques such as multithreading and parallelism to distribute tasks among the available processors. Modern operating systems, such as Linux, Windows, and macOS, are capable of managing SMP systems and can automatically distribute workloads across multiple processors or cores.

* * *

**You:**

What are difference between primary and seconday CPU cores?

* * *

**ChatGPT:**

In the context of multi-core or multi-processor systems, primary and secondary CPU cores generally refer to the roles these cores play in the system, with the primary core being responsible for the initialization process and secondary cores assisting in processing tasks once the system is up and running.

Here are the main differences between primary and secondary CPU cores:

1.  Initialization and Boot-up: The primary CPU core (sometimes called the boot core or master core) is responsible for initializing the system during boot-up. It executes the initial instructions, loads the firmware or BIOS, and configures the hardware components. Once the system is initialized, the primary core starts the operating system and enables other secondary cores.
    
2.  Secondary Core Activation: Secondary cores (also called slave cores or worker cores) are enabled by the primary core after the system initialization process is complete. They start to execute tasks assigned by the primary core or the operating system.
    
3.  Task Management: The primary core typically manages tasks and distributes them among secondary cores. However, modern operating systems can manage tasks independently and distribute them across all available cores (including the primary core) for efficient processing.
    
4.  Power Management: In some systems, the primary core may have more advanced power management capabilities compared to secondary cores, enabling it to control the power states of secondary cores, such as turning them off during periods of low workload to save power.
    

It is essential to note that these differences apply primarily to systems where a distinction is made between primary and secondary cores. In modern symmetric multiprocessing (SMP) systems, all cores are often treated as equals once the system is up and running, and the operating system manages tasks and power states across all cores without any significant difference in their roles.

* * *

**You:**

Please summarize the two types of CPU cores as a table.

* * *

**ChatGPT:**

| Aspect | Primary Core (Boot/Master Core) | Secondary Core (Slave/Worker Core) |
| --- | --- | --- |
| Initialization | Responsible for system initialization during boot-up | Activated by the primary core after system initialization |
| Task Management | Manages and distributes tasks among secondary cores | Executes tasks assigned by the primary core or OS |
| Power Management | May have advanced power management capabilities | Power states controlled by the primary core or OS |
| Core Activation | Always active during boot-up and system operation | Activated and deactivated as needed for workload demands |

Please note that in modern symmetric multiprocessing (SMP) systems, these distinctions become less relevant, as all cores are treated as equals once the system is up and running, and the operating system manages tasks and power states across all cores without any significant difference in their roles.