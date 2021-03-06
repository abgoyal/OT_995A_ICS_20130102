# Copyright 2011 the V8 project authors. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of Google Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

{
  'variables': {
    'use_system_v8%': 0,
    'msvs_use_common_release': 0,
    'gcc_version%': 'unknown',
    'v8_compress_startup_data%': 'off',
    'v8_target_arch%': '<(target_arch)',

    # Setting 'v8_can_use_unaligned_accesses' to 'true' will allow the code
    # generated by V8 to do unaligned memory access, and setting it to 'false'
    # will ensure that the generated code will always do aligned memory
    # accesses. The default value of 'default' will try to determine the correct
    # setting. Note that for Intel architectures (ia32 and x64) unaligned memory
    # access is allowed for all CPUs.
    'v8_can_use_unaligned_accesses%': 'default',

    # Setting 'v8_can_use_vfp_instructions' to 'true' will enable use of ARM VFP
    # instructions in the V8 generated code. VFP instructions will be enabled
    # both for the snapshot and for the ARM target. Leaving the default value
    # of 'false' will avoid VFP instructions in the snapshot and use CPU feature
    # probing when running on the target.
    'v8_can_use_vfp_instructions%': 'false',

    # Setting v8_use_arm_eabi_hardfloat to true will turn on V8 support for ARM
    # EABI calling convention where double arguments are passed in VFP
    # registers. Note that the GCC flag '-mfloat-abi=hard' should be used as
    # well when compiling for the ARM target.
    'v8_use_arm_eabi_hardfloat%': 'false',

    'v8_use_snapshot%': 'true',
    'host_os%': '<(OS)',
    'v8_use_liveobjectlist%': 'false',
  },
  'conditions': [
    ['use_system_v8==0', {
      'target_defaults': {
        'defines': [
          'ENABLE_LOGGING_AND_PROFILING',
          'ENABLE_DEBUGGER_SUPPORT',
          'ENABLE_VMSTATE_TRACKING',
          'V8_FAST_TLS',
        ],
        'conditions': [
          ['OS!="mac"', {
            # TODO(mark): The OS!="mac" conditional is temporary. It can be
            # removed once the Mac Chromium build stops setting target_arch to
            # ia32 and instead sets it to mac. Other checks in this file for
            # OS=="mac" can be removed at that time as well. This can be cleaned
            # up once http://crbug.com/44205 is fixed.
            'conditions': [
              ['v8_target_arch=="arm"', {
                'defines': [
                  'V8_TARGET_ARCH_ARM',
                ],
                'conditions': [
                  [ 'v8_can_use_unaligned_accesses=="true"', {
                    'defines': [
                      'CAN_USE_UNALIGNED_ACCESSES=1',
                    ],
                  }],
                  [ 'v8_can_use_unaligned_accesses=="false"', {
                    'defines': [
                      'CAN_USE_UNALIGNED_ACCESSES=0',
                    ],
                  }],
                  [ 'v8_can_use_vfp_instructions=="true"', {
                    'defines': [
                      'CAN_USE_VFP_INSTRUCTIONS',
                    ],
                  }],
                  [ 'v8_use_arm_eabi_hardfloat=="true"', {
                    'defines': [
                      'USE_EABI_HARDFLOAT=1',
                      'CAN_USE_VFP_INSTRUCTIONS',
                    ],
                  }],
                ],
              }],
              ['v8_target_arch=="ia32"', {
                'defines': [
                  'V8_TARGET_ARCH_IA32',
                ],
              }],
              ['v8_target_arch=="x64"', {
                'defines': [
                  'V8_TARGET_ARCH_X64',
                ],
              }],
            ],
          }],
          ['v8_use_liveobjectlist=="true"', {
            'defines': [
              'ENABLE_DEBUGGER_SUPPORT',
              'INSPECTOR',
              'OBJECT_PRINT',
              'LIVEOBJECTLIST',
            ],
          }],
         ['v8_compress_startup_data=="bz2"', {
            'defines': [
              'COMPRESS_STARTUP_DATA_BZ2',
            ],
          }],
        ],
        'configurations': {
          'Debug': {
            'defines': [
              'DEBUG',
              '_DEBUG',
              'ENABLE_DISASSEMBLER',
              'V8_ENABLE_CHECKS',
              'OBJECT_PRINT',
            ],
            'msvs_settings': {
              'VCCLCompilerTool': {
                'Optimization': '0',

                'conditions': [
                  ['OS=="win" and component=="shared_library"', {
                    'RuntimeLibrary': '3',  # /MDd
                  }, {
                    'RuntimeLibrary': '1',  # /MTd
                  }],
                ],
              },
              'VCLinkerTool': {
                'LinkIncremental': '2',
              },
            },
            'conditions': [
             ['OS=="freebsd" or OS=="openbsd"', {
               'cflags': [ '-I/usr/local/include' ],
             }],
           ],
          },
          'Release': {
            'conditions': [
              ['OS=="linux" or OS=="freebsd" or OS=="openbsd"', {
                'cflags!': [
                  '-O2',
                  '-Os',
                ],
                'cflags': [
                  '-fomit-frame-pointer',
                  '-O3',
                ],
                'conditions': [
                  [ 'gcc_version==44', {
                    'cflags': [
                      # Avoid crashes with gcc 4.4 in the v8 test suite.
                      '-fno-tree-vrp',
                    ],
                  }],
                ],
              }],
             ['OS=="freebsd" or OS=="openbsd"', {
               'cflags': [ '-I/usr/local/include' ],
             }],
              ['OS=="mac"', {
                'xcode_settings': {
                  'GCC_OPTIMIZATION_LEVEL': '3',  # -O3

                  # -fstrict-aliasing.  Mainline gcc
                  # enables this at -O2 and above,
                  # but Apple gcc does not unless it
                  # is specified explicitly.
                  'GCC_STRICT_ALIASING': 'YES',
                },
              }],
              ['OS=="win"', {
                'msvs_configuration_attributes': {
                  'OutputDirectory': '$(SolutionDir)$(ConfigurationName)',
                  'IntermediateDirectory': '$(OutDir)\\obj\\$(ProjectName)',
                  'CharacterSet': '1',
                },
                'msvs_settings': {
                  'VCCLCompilerTool': {
                    'Optimization': '2',
                    'InlineFunctionExpansion': '2',
                    'EnableIntrinsicFunctions': 'true',
                    'FavorSizeOrSpeed': '0',
                    'OmitFramePointers': 'true',
                    'StringPooling': 'true',

                    'conditions': [
                      ['OS=="win" and component=="shared_library"', {
                        'RuntimeLibrary': '2',  #/MD
                      }, {
                        'RuntimeLibrary': '0',  #/MT
                      }],
                    ],
                  },
                  'VCLinkerTool': {
                    'LinkIncremental': '1',
                    'OptimizeReferences': '2',
                    'OptimizeForWindows98': '1',
                    'EnableCOMDATFolding': '2',
                  },
                },
              }],
            ],
          },
        },
      },
      'targets': [
        {
          'target_name': 'v8',
          'toolsets': ['host', 'target'],
          'conditions': [
            ['v8_use_snapshot=="true"', {
              'dependencies': ['v8_snapshot'],
            },
            {
              'dependencies': ['v8_nosnapshot'],
            }],
            ['component=="shared_library"', {
              'type': '<(component)',
              'sources': [
                # Note: on non-Windows we still build this file so that gyp
                # has some sources to link into the component.
                '../../src/v8dll-main.cc',
              ],
              'conditions': [
                ['OS=="win"', {
                  'defines': [
                    'BUILDING_V8_SHARED',
                  ],
                  'direct_dependent_settings': {
                    'defines': [
                      'USING_V8_SHARED',
                    ],
                  },
                }, {
                  'defines': [
                    'V8_SHARED',
                  ],
                  'direct_dependent_settings': {
                    'defines': [
                      'V8_SHARED',
                    ],
                  },
                }],
              ],
            },
            {
              'type': 'none',
            }],
          ],
          'direct_dependent_settings': {
            'include_dirs': [
               '../../include',
            ],
          },
        },
        {
          'target_name': 'v8_snapshot',
          'type': '<(library)',
          'toolsets': ['host', 'target'],
          'conditions': [
            ['component=="shared_library"', {
              'conditions': [
                ['OS=="win"', {
                  'defines': [
                    'BUILDING_V8_SHARED',
                  ],
                  'direct_dependent_settings': {
                    'defines': [
                      'USING_V8_SHARED',
                    ],
                  },
                }, {
                  'defines': [
                    'V8_SHARED',
                  ],
                  'direct_dependent_settings': {
                    'defines': [
                      'V8_SHARED',
                    ],
                  },
                }],
              ],
            }],
          ],
          'dependencies': [
            'mksnapshot#host',
            'js2c#host',
            'v8_base',
          ],
          'include_dirs+': [
            '../../src',
          ],
          'sources': [
            '<(SHARED_INTERMEDIATE_DIR)/libraries.cc',
            '<(SHARED_INTERMEDIATE_DIR)/experimental-libraries.cc',
            '<(INTERMEDIATE_DIR)/snapshot.cc',
          ],
          'actions': [
            {
              'action_name': 'run_mksnapshot',
              'inputs': [
                '<(PRODUCT_DIR)/<(EXECUTABLE_PREFIX)mksnapshot<(EXECUTABLE_SUFFIX)',
              ],
              'outputs': [
                '<(INTERMEDIATE_DIR)/snapshot.cc',
              ],
              'variables': {
                'mksnapshot_flags': [],
              },
              'conditions': [
                ['v8_target_arch=="arm"', {
                  # The following rules should be consistent with chromium's
                  # common.gypi and V8's runtime rule to ensure they all generate
                  # the same correct machine code. The following issue is about
                  # V8's runtime rule about vfpv3 and neon:
                  # http://code.google.com/p/v8/issues/detail?id=914
                  'conditions': [
                    ['armv7==1', {
                      # The ARM Architecture Manual mandates VFPv3 if NEON is
                      # available.
                      # The current V8 doesn't use d16-d31, so for vfpv3-d16, we can
                      # also enable vfp3 for the better performance.
                      'conditions': [
                        ['arm_neon!=1 and arm_fpu!="vfpv3" and arm_fpu!="vfpv3-d16"', {
                          'variables': {
                            'mksnapshot_flags': [
                              '--noenable_vfp3',
                            ],
                          },
                        }],
                      ],
                    },{ # else: armv7!=1
                      'variables': {
                        'mksnapshot_flags': [
                          '--noenable_armv7',
                          '--noenable_vfp3',
                        ],
                      },
                    }],
                  ],
                }],
              ],
              'action': [
                '<@(_inputs)',
                '<@(mksnapshot_flags)',
                '<@(_outputs)'
              ],
            },
          ],
        },
        {
          'target_name': 'v8_nosnapshot',
          'type': '<(library)',
          'toolsets': ['host', 'target'],
          'dependencies': [
            'js2c#host',
            'v8_base',
          ],
          'include_dirs+': [
            '../../src',
          ],
          'sources': [
            '<(SHARED_INTERMEDIATE_DIR)/libraries.cc',
            '<(SHARED_INTERMEDIATE_DIR)/experimental-libraries.cc',
            '../../src/snapshot-empty.cc',
          ],
          'conditions': [
            # The ARM assembler assumes the host is 32 bits, so force building
            # 32-bit host tools.
            ['v8_target_arch=="arm" and host_arch=="x64" and _toolset=="host"', {
              'cflags': ['-m32'],
              'ldflags': ['-m32'],
            }],
            ['component=="shared_library"', {
              'defines': [
                'BUILDING_V8_SHARED',
                'V8_SHARED',
              ],
            }],
          ]
        },
        {
          'target_name': 'v8_base',
          'type': '<(library)',
          'toolsets': ['host', 'target'],
          'include_dirs+': [
            '../../src',
          ],
          'sources': [
            '../../src/accessors.cc',
            '../../src/accessors.h',
            '../../src/allocation.cc',
            '../../src/allocation.h',
            '../../src/api.cc',
            '../../src/api.h',
            '../../src/apiutils.h',
            '../../src/arguments.h',
            '../../src/assembler.cc',
            '../../src/assembler.h',
            '../../src/ast.cc',
            '../../src/ast-inl.h',
            '../../src/ast.h',
            '../../src/atomicops_internals_x86_gcc.cc',
            '../../src/bignum.cc',
            '../../src/bignum.h',
            '../../src/bignum-dtoa.cc',
            '../../src/bignum-dtoa.h',
            '../../src/bootstrapper.cc',
            '../../src/bootstrapper.h',
            '../../src/builtins.cc',
            '../../src/builtins.h',
            '../../src/bytecodes-irregexp.h',
            '../../src/cached-powers.cc',
            '../../src/cached-powers.h',
            '../../src/char-predicates-inl.h',
            '../../src/char-predicates.h',
            '../../src/checks.cc',
            '../../src/checks.h',
            '../../src/circular-queue-inl.h',
            '../../src/circular-queue.cc',
            '../../src/circular-queue.h',
            '../../src/code-stubs.cc',
            '../../src/code-stubs.h',
            '../../src/code.h',
            '../../src/codegen-inl.h',
            '../../src/codegen.cc',
            '../../src/codegen.h',
            '../../src/compilation-cache.cc',
            '../../src/compilation-cache.h',
            '../../src/compiler.cc',
            '../../src/compiler.h',
            '../../src/contexts.cc',
            '../../src/contexts.h',
            '../../src/conversions-inl.h',
            '../../src/conversions.cc',
            '../../src/conversions.h',
            '../../src/counters.cc',
            '../../src/counters.h',
            '../../src/cpu.h',
            '../../src/cpu-profiler-inl.h',
            '../../src/cpu-profiler.cc',
            '../../src/cpu-profiler.h',
            '../../src/data-flow.cc',
            '../../src/data-flow.h',
            '../../src/dateparser.cc',
            '../../src/dateparser.h',
            '../../src/dateparser-inl.h',
            '../../src/debug.cc',
            '../../src/debug.h',
            '../../src/debug-agent.cc',
            '../../src/debug-agent.h',
            '../../src/deoptimizer.cc',
            '../../src/deoptimizer.h',
            '../../src/disasm.h',
            '../../src/disassembler.cc',
            '../../src/disassembler.h',
            '../../src/dtoa.cc',
            '../../src/dtoa.h',
            '../../src/diy-fp.cc',
            '../../src/diy-fp.h',
            '../../src/double.h',
            '../../src/execution.cc',
            '../../src/execution.h',
            '../../src/factory.cc',
            '../../src/factory.h',
            '../../src/fast-dtoa.cc',
            '../../src/fast-dtoa.h',
            '../../src/flag-definitions.h',
            '../../src/fixed-dtoa.cc',
            '../../src/fixed-dtoa.h',
            '../../src/flags.cc',
            '../../src/flags.h',
            '../../src/frames-inl.h',
            '../../src/frames.cc',
            '../../src/frames.h',
            '../../src/full-codegen.cc',
            '../../src/full-codegen.h',
            '../../src/func-name-inferrer.cc',
            '../../src/func-name-inferrer.h',
            '../../src/global-handles.cc',
            '../../src/global-handles.h',
            '../../src/globals.h',
            '../../src/handles-inl.h',
            '../../src/handles.cc',
            '../../src/handles.h',
            '../../src/hashmap.cc',
            '../../src/hashmap.h',
            '../../src/heap-inl.h',
            '../../src/heap.cc',
            '../../src/heap.h',
            '../../src/heap-profiler.cc',
            '../../src/heap-profiler.h',
            '../../src/hydrogen.cc',
            '../../src/hydrogen.h',
            '../../src/hydrogen-instructions.cc',
            '../../src/hydrogen-instructions.h',
            '../../src/ic-inl.h',
            '../../src/ic.cc',
            '../../src/ic.h',
            '../../src/inspector.cc',
            '../../src/inspector.h',
            '../../src/interpreter-irregexp.cc',
            '../../src/interpreter-irregexp.h',
            '../../src/json-parser.h',
            '../../src/jsregexp.cc',
            '../../src/jsregexp.h',
            '../../src/isolate.cc',
            '../../src/isolate.h',
            '../../src/list-inl.h',
            '../../src/list.h',
            '../../src/lithium.cc',
            '../../src/lithium.h',
            '../../src/lithium-allocator.cc',
            '../../src/lithium-allocator.h',
            '../../src/lithium-allocator-inl.h',
            '../../src/liveedit.cc',
            '../../src/liveedit.h',
            '../../src/liveobjectlist-inl.h',
            '../../src/liveobjectlist.cc',
            '../../src/liveobjectlist.h',
            '../../src/log-inl.h',
            '../../src/log-utils.cc',
            '../../src/log-utils.h',
            '../../src/log.cc',
            '../../src/log.h',
            '../../src/macro-assembler.h',
            '../../src/mark-compact.cc',
            '../../src/mark-compact.h',
            '../../src/messages.cc',
            '../../src/messages.h',
            '../../src/natives.h',
            '../../src/objects-debug.cc',
            '../../src/objects-printer.cc',
            '../../src/objects-inl.h',
            '../../src/objects-visiting.cc',
            '../../src/objects-visiting.h',
            '../../src/objects.cc',
            '../../src/objects.h',
            '../../src/parser.cc',
            '../../src/parser.h',
            '../../src/platform-tls-mac.h',
            '../../src/platform-tls-win32.h',
            '../../src/platform-tls.h',
            '../../src/platform.h',
            '../../src/preparse-data-format.h',
            '../../src/preparse-data.cc',
            '../../src/preparse-data.h',
            '../../src/preparser.cc',
            '../../src/preparser.h',
            '../../src/prettyprinter.cc',
            '../../src/prettyprinter.h',
            '../../src/property.cc',
            '../../src/property.h',
            '../../src/profile-generator-inl.h',
            '../../src/profile-generator.cc',
            '../../src/profile-generator.h',
            '../../src/regexp-macro-assembler-irregexp-inl.h',
            '../../src/regexp-macro-assembler-irregexp.cc',
            '../../src/regexp-macro-assembler-irregexp.h',
            '../../src/regexp-macro-assembler-tracer.cc',
            '../../src/regexp-macro-assembler-tracer.h',
            '../../src/regexp-macro-assembler.cc',
            '../../src/regexp-macro-assembler.h',
            '../../src/regexp-stack.cc',
            '../../src/regexp-stack.h',
            '../../src/rewriter.cc',
            '../../src/rewriter.h',
            '../../src/runtime.cc',
            '../../src/runtime.h',
            '../../src/runtime-profiler.cc',
            '../../src/runtime-profiler.h',
            '../../src/safepoint-table.cc',
            '../../src/safepoint-table.h',
            '../../src/scanner-base.cc',
            '../../src/scanner-base.h',
            '../../src/scanner.cc',
            '../../src/scanner.h',
            '../../src/scopeinfo.cc',
            '../../src/scopeinfo.h',
            '../../src/scopes.cc',
            '../../src/scopes.h',
            '../../src/serialize.cc',
            '../../src/serialize.h',
            '../../src/shell.h',
            '../../src/small-pointer-list.h',
            '../../src/smart-pointer.h',
            '../../src/snapshot-common.cc',
            '../../src/snapshot.h',
            '../../src/spaces-inl.h',
            '../../src/spaces.cc',
            '../../src/spaces.h',
            '../../src/string-search.cc',
            '../../src/string-search.h',
            '../../src/string-stream.cc',
            '../../src/string-stream.h',
            '../../src/strtod.cc',
            '../../src/strtod.h',
            '../../src/stub-cache.cc',
            '../../src/stub-cache.h',
            '../../src/token.cc',
            '../../src/token.h',
            '../../src/type-info.cc',
            '../../src/type-info.h',
            '../../src/unbound-queue-inl.h',
            '../../src/unbound-queue.h',
            '../../src/unicode-inl.h',
            '../../src/unicode.cc',
            '../../src/unicode.h',
            '../../src/utils-inl.h',
            '../../src/utils.cc',
            '../../src/utils.h',
            '../../src/v8-counters.cc',
            '../../src/v8-counters.h',
            '../../src/v8.cc',
            '../../src/v8.h',
            '../../src/v8checks.h',
            '../../src/v8conversions.cc',
            '../../src/v8conversions.h',
            '../../src/v8globals.h',
            '../../src/v8memory.h',
            '../../src/v8threads.cc',
            '../../src/v8threads.h',
            '../../src/v8utils.cc',
            '../../src/v8utils.h',
            '../../src/variables.cc',
            '../../src/variables.h',
            '../../src/version.cc',
            '../../src/version.h',
            '../../src/vm-state-inl.h',
            '../../src/vm-state.h',
            '../../src/zone-inl.h',
            '../../src/zone.cc',
            '../../src/zone.h',
            '../../src/extensions/externalize-string-extension.cc',
            '../../src/extensions/externalize-string-extension.h',
            '../../src/extensions/gc-extension.cc',
            '../../src/extensions/gc-extension.h',
          ],
          'conditions': [
            ['v8_target_arch=="arm"', {
              'include_dirs+': [
                '../../src/arm',
              ],
              'sources': [
                '../../src/arm/assembler-arm-inl.h',
                '../../src/arm/assembler-arm.cc',
                '../../src/arm/assembler-arm.h',
                '../../src/arm/builtins-arm.cc',
                '../../src/arm/code-stubs-arm.cc',
                '../../src/arm/code-stubs-arm.h',
                '../../src/arm/codegen-arm.cc',
                '../../src/arm/codegen-arm.h',
                '../../src/arm/constants-arm.h',
                '../../src/arm/constants-arm.cc',
                '../../src/arm/cpu-arm.cc',
                '../../src/arm/debug-arm.cc',
                '../../src/arm/deoptimizer-arm.cc',
                '../../src/arm/disasm-arm.cc',
                '../../src/arm/frames-arm.cc',
                '../../src/arm/frames-arm.h',
                '../../src/arm/full-codegen-arm.cc',
                '../../src/arm/ic-arm.cc',
                '../../src/arm/lithium-arm.cc',
                '../../src/arm/lithium-arm.h',
                '../../src/arm/lithium-codegen-arm.cc',
                '../../src/arm/lithium-codegen-arm.h',
                '../../src/arm/lithium-gap-resolver-arm.cc',
                '../../src/arm/lithium-gap-resolver-arm.h',
                '../../src/arm/macro-assembler-arm.cc',
                '../../src/arm/macro-assembler-arm.h',
                '../../src/arm/regexp-macro-assembler-arm.cc',
                '../../src/arm/regexp-macro-assembler-arm.h',
                '../../src/arm/simulator-arm.cc',
                '../../src/arm/stub-cache-arm.cc',
              ],
              'conditions': [
                # The ARM assembler assumes the host is 32 bits,
                # so force building 32-bit host tools.
                ['host_arch=="x64" and _toolset=="host"', {
                  'cflags': ['-m32'],
                  'ldflags': ['-m32'],
                }]
              ]
            }],
            ['v8_target_arch=="ia32" or v8_target_arch=="mac" or OS=="mac"', {
              'include_dirs+': [
                '../../src/ia32',
              ],
              'sources': [
                '../../src/ia32/assembler-ia32-inl.h',
                '../../src/ia32/assembler-ia32.cc',
                '../../src/ia32/assembler-ia32.h',
                '../../src/ia32/builtins-ia32.cc',
                '../../src/ia32/code-stubs-ia32.cc',
                '../../src/ia32/code-stubs-ia32.h',
                '../../src/ia32/codegen-ia32.cc',
                '../../src/ia32/codegen-ia32.h',
                '../../src/ia32/cpu-ia32.cc',
                '../../src/ia32/debug-ia32.cc',
                '../../src/ia32/deoptimizer-ia32.cc',
                '../../src/ia32/disasm-ia32.cc',
                '../../src/ia32/frames-ia32.cc',
                '../../src/ia32/frames-ia32.h',
                '../../src/ia32/full-codegen-ia32.cc',
                '../../src/ia32/ic-ia32.cc',
                '../../src/ia32/lithium-codegen-ia32.cc',
                '../../src/ia32/lithium-codegen-ia32.h',
                '../../src/ia32/lithium-gap-resolver-ia32.cc',
                '../../src/ia32/lithium-gap-resolver-ia32.h',
                '../../src/ia32/lithium-ia32.cc',
                '../../src/ia32/lithium-ia32.h',
                '../../src/ia32/macro-assembler-ia32.cc',
                '../../src/ia32/macro-assembler-ia32.h',
                '../../src/ia32/regexp-macro-assembler-ia32.cc',
                '../../src/ia32/regexp-macro-assembler-ia32.h',
                '../../src/ia32/stub-cache-ia32.cc',
              ],
            }],
            ['v8_target_arch=="x64" or v8_target_arch=="mac" or OS=="mac"', {
              'include_dirs+': [
                '../../src/x64',
              ],
              'sources': [
                '../../src/x64/assembler-x64-inl.h',
                '../../src/x64/assembler-x64.cc',
                '../../src/x64/assembler-x64.h',
                '../../src/x64/builtins-x64.cc',
                '../../src/x64/code-stubs-x64.cc',
                '../../src/x64/code-stubs-x64.h',
                '../../src/x64/codegen-x64.cc',
                '../../src/x64/codegen-x64.h',
                '../../src/x64/cpu-x64.cc',
                '../../src/x64/debug-x64.cc',
                '../../src/x64/deoptimizer-x64.cc',
                '../../src/x64/disasm-x64.cc',
                '../../src/x64/frames-x64.cc',
                '../../src/x64/frames-x64.h',
                '../../src/x64/full-codegen-x64.cc',
                '../../src/x64/ic-x64.cc',
                '../../src/x64/lithium-codegen-x64.cc',
                '../../src/x64/lithium-codegen-x64.h',
                '../../src/x64/lithium-gap-resolver-x64.cc',
                '../../src/x64/lithium-gap-resolver-x64.h',
                '../../src/x64/lithium-x64.cc',
                '../../src/x64/lithium-x64.h',
                '../../src/x64/macro-assembler-x64.cc',
                '../../src/x64/macro-assembler-x64.h',
                '../../src/x64/regexp-macro-assembler-x64.cc',
                '../../src/x64/regexp-macro-assembler-x64.h',
                '../../src/x64/stub-cache-x64.cc',
              ],
            }],
            ['OS=="linux"', {
                'link_settings': {
                  'libraries': [
                    # Needed for clock_gettime() used by src/platform-linux.cc.
                    '-lrt',
                  ],
                  'conditions': [
                    ['v8_compress_startup_data=="bz2"', {
                      'libraries': [
                        '-lbz2',
                    ]}],
                  ],
                },
                'sources': [
                  '../../src/platform-linux.cc',
                  '../../src/platform-posix.cc'
                ],
              }
            ],
            ['OS=="android"', {
                'sources': [
                  '../../src/platform-posix.cc',
                ],
                'conditions': [
                  ['host_os=="mac" and _toolset!="target"', {
                    'sources': [
                      '../../src/platform-macos.cc'
                    ]
                  }, {
                    'sources': [
                      '../../src/platform-linux.cc'
                    ]
                  }],
                  ['_toolset=="target"', {
                    'link_settings': {
                      'libraries': [
                        '-llog',
                       ],
                     }
                  }],
                ],
              },
            ],
            ['OS=="freebsd"', {
                'link_settings': {
                  'libraries': [
                    '-L/usr/local/lib -lexecinfo',
                ]},
                'sources': [
                  '../../src/platform-freebsd.cc',
                  '../../src/platform-posix.cc'
                ],
              }
            ],
            ['OS=="openbsd"', {
                'link_settings': {
                  'libraries': [
                    '-L/usr/local/lib -lexecinfo',
                ]},
                'sources': [
                  '../../src/platform-openbsd.cc',
                  '../../src/platform-posix.cc'
                ],
              }
            ],
            ['OS=="mac"', {
              'sources': [
                '../../src/platform-macos.cc',
                '../../src/platform-posix.cc'
              ]},
            ],
            ['OS=="win"', {
              'sources': [
                '../../src/platform-win32.cc',
              ],
              'msvs_disabled_warnings': [4351, 4355, 4800],
              'link_settings':  {
                'libraries': [ '-lwinmm.lib' ],
              },
            }],
            ['component=="shared_library"', {
              'defines': [
                'BUILDING_V8_SHARED',
                'V8_SHARED',
              ],
            }],
          ],
        },
        {
          'target_name': 'js2c',
          'type': 'none',
          'toolsets': ['host'],
          'variables': {
            'library_files': [
              '../../src/runtime.js',
              '../../src/v8natives.js',
              '../../src/array.js',
              '../../src/string.js',
              '../../src/uri.js',
              '../../src/math.js',
              '../../src/messages.js',
              '../../src/apinatives.js',
              '../../src/debug-debugger.js',
              '../../src/mirror-debugger.js',
              '../../src/liveedit-debugger.js',
              '../../src/date.js',
              '../../src/json.js',
              '../../src/regexp.js',
              '../../src/macros.py',
            ],
            'experimental_library_files': [
              '../../src/proxy.js',
              '../../src/macros.py',
            ],
          },
          'actions': [
            {
              'action_name': 'js2c',
              'inputs': [
                '../../tools/js2c.py',
                '<@(library_files)',
              ],
              'outputs': [
                '<(SHARED_INTERMEDIATE_DIR)/libraries.cc',
              ],
              'action': [
                'python',
                '../../tools/js2c.py',
                '<@(_outputs)',
                'CORE',
                '<(v8_compress_startup_data)',
                '<@(library_files)'
              ],
            },
            {
              'action_name': 'js2c_experimental',
              'inputs': [
                '../../tools/js2c.py',
                '<@(experimental_library_files)',
              ],
              'outputs': [
                '<(SHARED_INTERMEDIATE_DIR)/experimental-libraries.cc',
              ],
              'action': [
                'python',
                '../../tools/js2c.py',
                '<@(_outputs)',
                'EXPERIMENTAL',
                '<(v8_compress_startup_data)',
                '<@(experimental_library_files)'
              ],
            },
          ],
        },
        {
          'target_name': 'mksnapshot',
          'type': 'executable',
          'toolsets': ['host'],
          'dependencies': [
            'v8_nosnapshot',
          ],
          'include_dirs+': [
            '../../src',
          ],
          'sources': [
            '../../src/mksnapshot.cc',
          ],
          'conditions': [
            # The ARM assembler assumes the host is 32 bits, so force building
            # 32-bit host tools.
            ['v8_target_arch=="arm" and host_arch=="x64" and _toolset=="host"', {
              'cflags': ['-m32'],
              'ldflags': ['-m32'],
            }],
            ['v8_compress_startup_data=="bz2"', {
              'libraries': [
                '-lbz2',
              ]}],
          ]
        },
        {
          'target_name': 'v8_shell',
          'type': 'executable',
          'toolsets': ['host'],
          'dependencies': [
            'v8'
          ],
          'sources': [
            '../../samples/shell.cc',
          ],
          'conditions': [
            ['OS=="win"', {
              # This could be gotten by not setting chromium_code, if that's OK.
              'defines': ['_CRT_SECURE_NO_WARNINGS'],
            }],
            ['v8_compress_startup_data=="bz2"', {
              'libraries': [
                '-lbz2',
              ]}],
          ],
        },
      ],
    }, { # use_system_v8 != 0
      'targets': [
        {
          'target_name': 'v8',
          'type': 'settings',
          'toolsets': ['host', 'target'],
          'link_settings': {
            'libraries': [
              '-lv8',
            ],
          },
        },
        {
          'target_name': 'v8_shell',
          'type': 'none',
          'toolsets': ['host'],
          'dependencies': [
            'v8'
          ],
        },
      ],
    }],
  ],
}
