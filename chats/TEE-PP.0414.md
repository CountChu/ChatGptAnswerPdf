**You:**

guid: 789e11f8-0a1d-4c6b-be6e-7f5142bb6e0e
create_time: 2023-04-14 09:13:41
GlobalPlatform Technology
TEE Protection Profile
Version 1.3

Contents
1 Introduction  7
1.1 Audience ... 7
1.2 IPR Disclaimer... 8
1.3 References  8
1.4 Terminology and Definitions .. 9
1.5 Abbreviations and Notations ... 12
1.6 Revision History .. 15
2 TOE Overview ... 16
2.1 TOE Type  16
2.2 TOE Description .. 17
2.2.1 Software Architecture of a TEE-enabled Device .. 17
2.2.2 Hardware Architecture of a TEE-enabled Device  18
2.3 Usage and Major Security Features of the TOE . 21
2.3.1 TEE Security Functionality ... 21
2.3.2 TOE Usage ... 22
2.3.3 TEE Time and Rollback PP-Module  23
2.3.4 TEE Debug PP-Module  23
2.4 Available Non-TOE Hardware/Software/Firmware . 23
2.5 Reference Device Life Cycle ... 24
3 Conformance Claims and Consistency Rationale .. 27
3.1 Conformance Claim to CC .. 27
3.2 Conformance Claim to a Package .. 27
3.3 Conformance Claim of the PP . 27
3.4 Conformance Statement . 27
3.5 Consistency Rationale for the PP-Modules  28
3.5.1 TEE Time and Rollback PP-Module  28
3.5.2 TEE Debug PP-Module  28
4 Security Problem Definition . 29
4.1 Assets .. 29
4.1.1 Core TEE PP  29
4.1.2 TEE Time and Rollback PP-Module  30
4.1.3 TEE Debug PP-Module  31
4.2 Users ... 32
4.2.1 Core TEE PP  32
4.2.2 TEE Time and Rollback PP-Module  32
4.2.3 TEE Debug PP-Module  32
4.3 Threats  32
4.3.1 Core TEE PP  34
4.3.2 TEE Time and Rollback PP-Module  36
4.3.3 TEE Debug PP-Module  37
4.4 Organisational Security Policies.. 38
4.4.1 Core TEE PP  38
4.4.2 TEE Time and Rollback PP-Module  38
4.4.3 TEE Debug PP-Module  38
4.5 Assumptions  39
4.5.1 Core TEE PP  39
4.5.2 TEE Time and Rollback PP-Module  40
4.5.3 TEE Debug PP-Module  40
4 / 107 TEE Protection Profile – Public release v1.3
Copyright  2016-2020 GlobalPlatform, Inc. All Rights Reserved.
The technology provided or described herein is subject to updates, revisions, and extensions by GlobalPlatform. Use of this
information is governed by the GlobalPlatform license agreement and any use inconsistent with that agreement is strictly
prohibited.
5 Security Objectives .. 41
5.1 Security Objectives for the TOE .. 41
5.1.1 Core TEE PP  41
5.1.2 TEE Time and Rollback PP-Module  44
5.1.3 TEE Debug PP-Module  44
5.2 Security Objectives for the Operational Environment . 44
5.2.1 Core TEE PP  45
5.2.2 TEE Time and Rollback PP-Module  46
5.2.3 TEE Debug PP-Module  46
5.3 Security Objectives Rationale . 47
5.3.1 Threats . 47
5.3.1.1 Core TEE PP ... 47
5.3.1.2 TEE Time and Rollback PP-Module  50
5.3.1.3 TEE Debug PP-Module ... 50
5.3.2 Organisational Security Policies... 50
5.3.2.1 Core TEE PP ... 50
5.3.3 Assumptions . 50
5.3.3.1 Core TEE PP ... 50
5.3.4 SPD and Security Objectives ... 51
6 Extended Requirements ... 55
6.1 FCS_RNG – Generation of Random Numbers ... 55
6.2 FPT_INI - TSF Initialisation . 56
6.3 AVA_VAN_AP Vulnerability Analysis .. 57
7 Security Requirements  59
7.1 Security Functional Requirements .. 59
7.1.1 Core TEE PP  59
7.1.1.1 Identification . 62
7.1.1.2 Confidentiality, Integrity, and Isolation . 63
7.1.1.3 Cryptography ... 66
7.1.1.4 Initialisation, Operation, and Firmware Integrity .. 68
7.1.1.5 TEE Identification . 70
7.1.1.6 Instance Time .. 71
7.1.1.7 Random Number Generator  72
7.1.1.8 Trusted Storage ... 72
7.1.2 TEE Time and Rollback PP-Module  75
7.1.2.1 Rollback Protection .. 75
7.1.2.2 TA Persistent Time .. 76
7.1.3 TEE Debug PP-Module  78
7.2 Security Assurance Requirements .. 81
7.3 Security Requirements Rationale 82
7.3.1 Objectives . 82
7.3.1.1 Security Objectives for the TOE .. 82
7.3.1.1.1 Core TEE PP 82
7.3.1.1.2 TEE Time and Rollback PP-Module 84
7.3.1.1.3 TEE Debug PP-Module 85
7.3.2 Rationale Tables of Security Objectives and SFRs . 85
7.3.3 Dependencies .. 88
7.3.3.1 SFRs Dependencies  88
7.3.3.2 Rationale for the Exclusion of Dependencies .. 90
7.3.3.3 SARs Dependencies  91
7.3.4 Rationale for the Security Assurance Requirements ... 92
TEE Protection Profile – Public release v1.3 5 / 107
Copyright  2016-2020 GlobalPlatform, Inc. All Rights Reserved.
The technology provided or described herein is subject to updates, revisions, and extensions by GlobalPlatform. Use of this
information is governed by the GlobalPlatform license agreement and any use inconsistent with that agreement is strictly
prohibited.
Annex A Application of Attack Potential to TEE  93
A.1 Attack Potential .. 93
A.1.1 Attack Potential Grid 94
A.1.2 Attack Potential Levels .98
A.2 Attackers’ Exploitation Profiles ... 99
A.2.1 Exploitation Profile 1 (Remote Attacker) 100
A.2.2 Exploitation Profile 2 (Local Layman Attacker) ..101
A.2.3 Exploitation Profile 3 (Local Proficient Attacker) 101
A.2.4 Exploitation Profile 4 (Local Proficient Attacker with Equipment) ..101
A.3 Examples of Hardware-based Attack Paths  102
A.3.1 Side Channel Analysis Attack 102
A.3.2 Fault Injection Attack ..102
A.3.3 External DRAM Probing .103
A.3.4 Unprotected Debug Interface .103
A.4 Examples of Software-based Attack Paths .. 104
A.4.1 Hardware Vulnerabilities Exploited by Software 104
A.4.2 Integer Errors .105
A.4.3 Buffer Overflow ..105
A.4.4 Unchecked User Input105
A.4.5 Race Condition / TOCTOU 106
A.4.6 Dangling Pointers ...106
A.4.7 Timing Attack .106
A.4.8 System Call Hooking ..107

* * *

**ChatGPT:**

GlobalPlatform Technology
TEE Protection Profile
Version 1.3

This document outlines the Trusted Execution Environment (TEE) Protection Profile, which is a set of security requirements and guidelines for TEE-enabled devices. The TEE Protection Profile is intended to establish a common security baseline for these devices and provide guidance to developers, manufacturers, and evaluators in creating secure and trustworthy products.

The document is divided into several sections, including an introduction, TOE overview, conformance claims and consistency rationale, security problem definition, security objectives, extended requirements, security requirements, and an annex on the application of attack potential to TEE.

The TEE Protection Profile covers various aspects of TEE-enabled devices, such as the software and hardware architecture, the usage and major security features, the reference device life cycle, and the required security functional and assurance requirements.

Additionally, this document discusses different threats and attack paths, as well as the corresponding security objectives and requirements for countering them. Examples of hardware and software-based attacks are provided, along with guidance on how to evaluate the attack potential and select appropriate countermeasures.

In summary, the TEE Protection Profile is an essential resource for those involved in the development, evaluation, and deployment of TEE-enabled devices, as it offers a comprehensive set of security requirements and guidelines to ensure a high level of security and trustworthiness.

* * *

**You:**

guid: 4d3b00e1-463e-4f14-97d7-1e540f477f06
create_time: 2023-04-14 09:15:05
What is PP?

* * *

**ChatGPT:**

PP stands for Protection Profile. In the context of information security and evaluation, a Protection Profile is a document that outlines a standardized set of security requirements for a specific class of products or systems. Protection Profiles are often used as a baseline for developers, manufacturers, and evaluators to create, assess, and compare the security of different products within the same category.

A Protection Profile typically includes information on the target of evaluation (TOE), security problem definition, security objectives, security requirements, and conformance claims. By adhering to a Protection Profile, product developers and manufacturers can ensure that their products meet a common set of security requirements, thus making it easier for customers and evaluators to assess and compare the security features of different products within the same class.

* * *

**You:**

guid: bead2ff9-cf60-446b-b5c5-2b616cece8b7
create_time: 2023-04-14 09:33:48
OE.ROLLBACK
TA developers shall not rely on the protection of TEE persistent data, TA data and keys, and TA code against rollback between two reset operations.
Application Note:
The core TEE PP enforces the consistency (i.e. runtime integrity) of TEE persistent data, TA data and keys, and TA code, but not their integrity between two reset operations.

* * *

**ChatGPT:**

OE.ROLLBACK is an organizational security policy stating that Trusted Application (TA) developers should not rely on the protection of TEE persistent data, TA data and keys, and TA code against rollback between two reset operations.

In the context of a Trusted Execution Environment (TEE), a rollback attack occurs when an attacker attempts to revert the state of a system or its data to an earlier point in time, which may allow them to exploit known vulnerabilities or bypass security measures that were implemented later.

The core TEE Protection Profile (PP) enforces the consistency (i.e., runtime integrity) of TEE persistent data, TA data and keys, and TA code, but it does not guarantee their integrity between two reset operations. This means that the TEE PP ensures that these data elements remain consistent and unaltered during runtime, but it does not protect them from being rolled back to a previous state after a reset operation.

As a result, TA developers should be aware of this limitation and not rely solely on the core TEE PP's protection mechanisms to prevent rollback attacks. They should implement additional security measures to mitigate the risk of such attacks and ensure the integrity of their TA data, keys, and code between reset operations.

* * *

