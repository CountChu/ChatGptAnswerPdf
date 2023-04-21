**You:**

https://software-dl.ti.com/jacinto7/esd/processor-sdk-linux-rt-jacinto7/08\_04\_00\_03/exports/docs/linux/Foundational\_Components\_OPTEE.html?highlight=trusted

* * *

**ChatGPT:**

I'm sorry, but as an AI language model, I cannot browse the web or access external links. However, I can try to help answer any questions you may have about the Texas Instruments Jacinto 7 Processor or OP-TEE (Open Portable Trusted Execution Environment).

The Texas Instruments Jacinto 7 Processor is an automotive processor designed for advanced driver assistance systems (ADAS) and in-vehicle infotainment (IVI) applications. It is a System-on-Chip (SoC) solution that integrates multiple processing cores, including Arm Cortex-A72 and Cortex-R5F cores, along with a TI C71x DSP and multiple accelerators for computer vision and deep learning tasks.

OP-TEE (Open Portable Trusted Execution Environment) is an open-source implementation of the TEE (Trusted Execution Environment) for Arm Cortex-A based processors. It provides a secure environment for executing trusted applications isolated from the normal operating system, ensuring confidentiality and integrity of sensitive data and applications.

If you have any specific questions about these topics, feel free to ask, and I'll do my best to help.

* * *

**You:**

3.10. OP-TEE Overview OP-TEE is a Trusted Execution Environment (TEE) designed as companion to a non-secure Linux kernel running on Arm; Cortex-A cores using the TrustZone technology. OP-TEE binary is compiled with U-Boot and following are the instructions for compiling and booting it. Furthur information about it can be found at: https://optee.readthedocs.io/en/latest/general/about.html Official OP-TEE documentation here. Getting the OP-TEE Source Code $ git clone https://github.com/OP-TEE/optee\_os.git Getting Security Dev Tool $ git clone https://git.ti.com/git/security-development-tools/core-secdev-k3.git -b master $ export TI\_SECURE\_DEV\_PKG=\`pwd\`/core-secdev-k3 Building OP-TEE On GP $ make CROSS\_COMPILE64=aarch64-linux-gnu- PLATFORM=k3-j721e CFG\_ARM64\_core=y With debug parameters $ make CROSS\_COMPILE64=aarch64-none-linux-gnu- PLATFORM=k3-j721e CFG\_ARM64\_core=y CFG\_TEE\_CORE\_LOG\_LEVEL=2 CFG\_TEE\_CORE\_DEBUG=y Sign image for HS $ {TI\_SECURE\_DEV\_PKG}/scripts/secure-binary-image.sh ./out/arm-plat-k3/core/tee-pager\_v2.bin ./out/arm-plat-k3/core/tee-pager\_v2.bin.signed Secure Storage with RPMB (For HS) OP-TEE provides secure storage functionality. TI SoCs with HS configuration have a KEK embedded in them that is programmed across OP-TEE instances that are distributed in a derived manner. Each HS device has its own signing key which is different from other HS devices. For enabling RPMB support along with secure storage, additional flags need to be passed to the build instructions. The information for the flags can be found here. https://optee.readthedocs.io/en/latest/architecture/secure\_storage.html There is a hybrid mode in which both the flags i.e CFG\_REE\_FS=y and CFG\_RPMB\_FS=y are enabled. This mode stores the state of the Secure Storage directory in RPMB partition to check for the integrity of the data present in it. It is the recommended way. E.g. For enabling hybrid mode of RPMB along with REE\_FS $ make CROSS\_COMPILE64=aarch64-linux-gnu- PLATFORM=k3-j721e CFG\_ARM64\_core=y CFG\_REE\_FS=y CFG\_RPMB\_FS=y $ {TI\_SECURE\_DEV\_PKG}/scripts/secure-binary-image.sh ./out/arm-plat-k3/core/tee-pager\_v2.bin ./out/arm-plat-k3/core/tee-pager\_v2.bin.signed OPTEE-client also needs to be updated to enable the use of real emmc instead of the virtual emmc that is enabled by default Getting OP-TEE Client source code $ git clone https://github.com/OP-TEE/optee\_client Building OP-TEE Client with RPMB support $ make CROSS\_COMPILE="aarch64-linux-gnu-" PLATFORM=k3 CFG\_TEE\_SUPP\_LOG\_LEVEL=2 RPMB\_EMU=0 CFG\_ARM64\_core=y Now update optee-client binary and libraries on your SD card with the generated ones in out/export/usr folder Building u-boot with OP-TEE os If building for an HS device, tee-pager\_v2.bin must be signed before it is packaged in tispl.bin. To sign the binary, the script secure-binary-image.sh is called as shown above with the path to the newly built binary: tee-pager\_v2.bin (the first argument) and with the expected output binary path and name: tee-pager\_v2.bin.signed (the second argument). Once the binary is signed, continue with the HS boot instructions found here: Build U-Boot. Expected binary output Generated binary: tee-pager\_v2.bin Binary saved saved in: <path-to-optee>/out/arm-plat-k3/core Integrate binary output into U-boot Go to u-boot folder <path-to-u-boot> Re-build U-boot with A72/A53 instructions found under: Build U-Boot, but with the TEE parameter pointing to the newly built tee-pager\_v2.bin. i.e. TEE=<path-to-optee>/out/arm-plat-k3/core/tee-pager\_v2.bin Note tee-pager\_v2.bin may be called bl32.bin in other documentation. © Copyright 1995-2021, Texas Instruments Incorporated. All rights reserved. Trademarks | Privacy policy | Terms of use | Terms of sale

* * *

**ChatGPT:**

Based on the information provided, the instructions explain how to build and integrate OP-TEE with the Jacinto 7 Processor for both GP and HS devices. Here's a summary of the steps:

1.  **Get the OP-TEE Source Code**: Clone the OP-TEE source code from GitHub.
2.  **Get the Security Dev Tool**: Clone the TI Security Development Tools repository and set the TI\_SECURE\_DEV\_PKG environment variable.
3.  **Build OP-TEE**: Build the OP-TEE binary for the k3-j721e platform using the provided commands.
4.  **Sign the image for HS**: If you are building for an HS device, sign the tee-pager\_v2.bin using the provided script.
5.  **Enable RPMB support and secure storage**: To enable RPMB support along with secure storage, additional flags need to be passed to the build instructions. You can enable the hybrid mode of RPMB along with REE\_FS by following the provided example.
6.  **Get and build the OP-TEE Client with RPMB support**: Clone the OP-TEE client source code and build it with the appropriate flags. Then, update the optee-client binary and libraries on your SD card with the generated ones in the out/export/usr folder.
7.  **Build U-Boot with OP-TEE OS**: Follow the instructions to build U-Boot with the TEE parameter pointing to the newly built tee-pager\_v2.bin.
8.  **Integrate binary output into U-Boot**: Re-build U-Boot with A72/A53 instructions found under "Build U-Boot," but with the TEE parameter pointing to the newly built tee-pager\_v2.bin.

Remember that tee-pager\_v2.bin may be referred to as bl32.bin in other documentation.

For additional information, you can refer to the official OP-TEE documentation at [https://optee.readthedocs.io/en/latest/](https://optee.readthedocs.io/en/latest/).

Please note that this is a summary of the instructions provided, and you should follow the detailed steps in the original text to build and integrate OP-TEE successfully.

* * *

**You:**

What is GP?

* * *

**ChatGPT:**

In the context of the instructions provided, "GP" refers to "General Purpose" devices. When discussing Texas Instruments (TI) processors, the term is used to differentiate between two types of devices: General Purpose (GP) and High Security (HS).

General Purpose (GP) devices are designed for a broad range of applications and use cases. They typically do not include the same level of security features as High Security (HS) devices.

High Security (HS) devices, on the other hand, are designed with additional security features and are intended for use in applications that require a higher level of security, such as automotive systems, industrial control systems, or other safety-critical applications.

When building OP-TEE for a Jacinto 7 Processor, you may need to follow different steps depending on whether you are targeting a General Purpose (GP) or High Security (HS) device. For example, the instructions provided mention signing the tee-pager\_v2.bin when building for an HS device, which is not required for a GP device.

* * *

**You:**

What is RPMB?

* * *

**ChatGPT:**

RPMB stands for Replay Protected Memory Block. It is a security feature provided in eMMC (embedded Multi-Media Controller) and UFS (Universal Flash Storage) devices. RPMB is designed to offer a secure, tamper-resistant storage area for sensitive data and to protect against replay attacks.

In the context of OP-TEE and secure storage, RPMB is used to store sensitive information in a protected environment, ensuring data confidentiality and integrity. It can be used in combination with other secure storage options, such as REE\_FS (Rich Execution Environment File System), to create a hybrid storage solution. The hybrid mode uses the Secure Storage directory in the RPMB partition to check for the integrity of the data present in it, providing an added layer of security.

When building OP-TEE with RPMB support, you need to pass additional flags to the build instructions, as mentioned in the provided steps. This enables the use of real eMMC storage instead of the default virtual eMMC storage.

* * *

**You:**

What is KEK?

* * *

**ChatGPT:**

KEK stands for Key Encryption Key. In cryptography and secure systems, a KEK is used to securely transmit and store encryption keys. The main purpose of a KEK is to protect the actual encryption keys (also known as data encryption keys or DEKs) that are used to encrypt and decrypt sensitive data.

The KEK is used to encrypt the DEKs before they are stored or transmitted, and only authorized systems with the correct KEK can decrypt the DEKs to access the actual encryption keys. This adds an additional layer of security, ensuring that even if the encrypted DEKs are intercepted or compromised, an attacker would still need the KEK to decrypt and use them.

In the context of TI SoCs (System-on-Chip) with High Security (HS) configuration, a KEK is embedded in the devices and programmed across OP-TEE instances. Each HS device has its own unique signing key, which is different from other HS devices. This further enhances the security of the overall system, making it more difficult for attackers to compromise the sensitive data stored within.

* * *

**You:**

Is a KEK unique for each device?

* * *

**ChatGPT:**

In the context of Texas Instruments (TI) System-on-Chip (SoC) devices with High Security (HS) configuration, each device does have a unique KEK (Key Encryption Key). This means that each HS device has its own signing key, which is different from other HS devices. This approach enhances the security of the overall system, making it more difficult for attackers to compromise the sensitive data stored within.

However, it's essential to understand that the uniqueness of a KEK depends on the specific implementation and the security requirements of the system. In some cases, KEKs may be shared among multiple devices or systems to enable secure communication between them.

In summary, while the KEKs in TI SoCs with HS configuration are unique for each device, the uniqueness of KEKs in other systems may vary depending on the specific implementation and security requirements.