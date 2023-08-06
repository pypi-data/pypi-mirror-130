# pubsubplus-python-client
#
# Copyright 2021 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=trailing-whitespace
"""This module contains dictionary keys for legacy properties."""

_GENERATE_RECEIVE_TIMESTAMPS_v1_0_0 = "solclient.session.prop.generate-rcv-timestamps"  # pylint: disable=invalid-name
"""_GENERATE_RECEIVE_TIMESTAMPS_v1_0_0 may be used as a legacy version of the
:py:class.`solace.messaging.config.solace_properties.service_properties.GENERATE_RECEIVE_TIMESTAMPS key."""

_GENERATE_SEND_TIMESTAMPS_v1_0_0 = "solclient.session.prop.generate-send-timestamps"  # pylint: disable=invalid-name
"""_GENERATE_SEND_TIMESTAMPS_v1_0_0 may be used as a legacy version of the
:py:class:`solace.messaging.config.solace_properties.service_properties.GENERATE_SEND_TIMESTAMPS key."""

_PERSISTENT_NO_LOCAL_PUBLISHED_MESSAGES_v1_0_0 = "solace.messaging.receiver.persistent.no-local-published-messages"  # pylint: disable=invalid-name
"""_PERSISTENT_NO_LOCAL_PUPLISHED_MESSAGES_v1_0_0 may be used as a legacy version of the
:py:class:`solace.messaging.config.solace_properties.receiver_properties.PERSISTENT_NO_LiOCAL_PUBLISHED_MESSAGES
key."""

_SEQUENCE_NUMBER_v1_0_0 = "solace.messaging.message.sequence-number"  # pylint: disable=invalid-name
"""_SEQUENCE_NUMBER_v1_0_0 can be used as a legacy version of the
:py:class:`solace.messaging.config.solace_properties.message_properties.SEQUENCE_NUMBER key."""
