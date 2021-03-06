# Copyright 2010 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

LOCAL_PATH:= $(call my-dir)

include $(CLEAR_VARS)
LOCAL_SRC_FILES := \
	alpha.c \
	bits.c \
	buffer.c \
	dsp.c \
	dsp_sse2.c \
	frame.c \
	idec.c \
	io.c \
	io_sse2.c \
	layer.c \
	quant.c \
	tree.c \
	vp8.c \
	webp.c \
	yuv.c

LOCAL_CFLAGS := -DANDROID

LOCAL_C_INCLUDES += \
	$(LOCAL_PATH) \
	$(LOCAL_PATH)/../../include

LOCAL_MODULE:= libwebp-decode

include $(BUILD_STATIC_LIBRARY)
