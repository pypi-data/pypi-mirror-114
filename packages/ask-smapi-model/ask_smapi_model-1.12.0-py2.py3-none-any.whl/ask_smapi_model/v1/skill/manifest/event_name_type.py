# coding: utf-8

#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#

import pprint
import re  # noqa: F401
import six
import typing
from enum import Enum


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime


class EventNameType(Enum):
    """
    Name of the event to be subscribed to.



    Allowed enum values: [Legacy_AudioPlayerGui_LyricsViewedEvent, Legacy_ListModel_DeleteItemRequest, Legacy_MediaPlayer_SequenceModified, Legacy_PlaybackController_ButtonCommand, EffectsController_RequestEffectChangeRequest, Legacy_ExternalMediaPlayer_RequestToken, ITEMS_UPDATED, Alexa_Video_Xray_ShowDetailsSuccessful, PlaybackController_NextCommandIssued, Legacy_MediaPlayer_PlaybackFinished, Alexa_Camera_VideoCaptureController_CaptureFailed, SKILL_DISABLED, Alexa_Camera_VideoCaptureController_CancelCaptureFailed, CustomInterfaceController_EventsReceived, Legacy_DeviceNotification_NotificationStarted, REMINDER_UPDATED, AUDIO_ITEM_PLAYBACK_STOPPED, Legacy_AuxController_InputActivityStateChanged, LocalApplication_MShopPurchasing_Event, Legacy_ExternalMediaPlayer_AuthorizationComplete, LocalApplication_HHOPhotos_Event, Alexa_Presentation_APL_UserEvent, Legacy_AudioPlayer_PlaybackInterrupted, Legacy_BluetoothNetwork_DeviceUnpairFailure, IN_SKILL_PRODUCT_SUBSCRIPTION_ENDED, Alexa_FileManager_UploadController_UploadFailed, Legacy_BluetoothNetwork_DeviceConnectedFailure, Legacy_AudioPlayer_AudioStutter, Alexa_Camera_VideoCaptureController_CaptureStarted, Legacy_Speaker_MuteChanged, CardRenderer_DisplayContentFinished, Legacy_SpeechSynthesizer_SpeechStarted, AudioPlayer_PlaybackStopped, Legacy_SoftwareUpdate_CheckSoftwareUpdateReport, CardRenderer_DisplayContentStarted, LocalApplication_NotificationsApp_Event, AudioPlayer_PlaybackStarted, Legacy_DeviceNotification_NotificationEnteredForground, Legacy_DeviceNotification_SetNotificationFailed, Legacy_AudioPlayer_PeriodicPlaybackProgressReport, Legacy_HomeAutoWifiController_HttpNotified, Alexa_Camera_PhotoCaptureController_CancelCaptureFailed, SKILL_ACCOUNT_LINKED, LIST_UPDATED, Legacy_DeviceNotification_NotificationSync, Legacy_SconeRemoteControl_VolumeDown, Legacy_MediaPlayer_PlaybackPaused, Legacy_Presentation_PresentationUserEvent, PlaybackController_PlayCommandIssued, Legacy_ListModel_UpdateItemRequest, Messaging_MessageReceived, Legacy_SoftwareUpdate_InitiateSoftwareUpdateReport, AUDIO_ITEM_PLAYBACK_FAILED, LocalApplication_DeviceMessaging_Event, Alexa_Camera_PhotoCaptureController_CaptureFailed, Legacy_AudioPlayer_PlaybackIdle, Legacy_BluetoothNetwork_EnterPairingModeSuccess, Legacy_AudioPlayer_PlaybackError, Legacy_ListModel_GetPageByOrdinalRequest, Legacy_MediaGrouping_GroupChangeResponseEvent, Legacy_BluetoothNetwork_DeviceDisconnectedFailure, Legacy_BluetoothNetwork_EnterPairingModeFailure, Legacy_SpeechSynthesizer_SpeechInterrupted, PlaybackController_PreviousCommandIssued, Legacy_AudioPlayer_PlaybackFinished, Legacy_System_UserInactivity, Display_UserEvent, Legacy_PhoneCallController_Event, Legacy_DeviceNotification_SetNotificationSucceeded, LocalApplication_Photos_Event, LocalApplication_VideoExperienceService_Event, Legacy_ContentManager_ContentPlaybackTerminated, Legacy_PlaybackController_PlayCommand, Legacy_PlaylistController_ErrorResponse, Legacy_SconeRemoteControl_VolumeUp, MessagingController_UpdateConversationsStatus, Legacy_BluetoothNetwork_DeviceDisconnectedSuccess, LocalApplication_Communications_Event, AUDIO_ITEM_PLAYBACK_STARTED, Legacy_BluetoothNetwork_DevicePairFailure, LIST_DELETED, Legacy_PlaybackController_ToggleCommand, Legacy_BluetoothNetwork_DevicePairSuccess, Legacy_MediaPlayer_PlaybackError, AudioPlayer_PlaybackFinished, Legacy_DeviceNotification_NotificationStopped, Legacy_SipClient_Event, Display_ElementSelected, LocalApplication_MShop_Event, Legacy_ListModel_AddItemRequest, Legacy_BluetoothNetwork_ScanDevicesReport, Legacy_MediaPlayer_PlaybackStopped, Legacy_AudioPlayerGui_ButtonClickedEvent, LocalApplication_AlexaVoiceLayer_Event, Legacy_PlaybackController_PreviousCommand, Legacy_AudioPlayer_InitialPlaybackProgressReport, Legacy_BluetoothNetwork_DeviceConnectedSuccess, LIST_CREATED, Legacy_ActivityManager_ActivityContextRemovedEvent, ALL_LISTS_CHANGED, Legacy_AudioPlayer_PlaybackNearlyFinished, Legacy_MediaGrouping_GroupChangeNotificationEvent, LocalApplication_Sentry_Event, SKILL_PROACTIVE_SUBSCRIPTION_CHANGED, REMINDER_CREATED, Alexa_Presentation_HTML_Event, FitnessSessionController_FitnessSessionError, Legacy_SconeRemoteControl_Next, Alexa_Camera_VideoCaptureController_CaptureFinished, Legacy_MediaPlayer_SequenceItemsRequested, Legacy_PlaybackController_PauseCommand, LocalApplication_AlexaVision_Event, LocalApplication_Closet_Event, Alexa_FileManager_UploadController_CancelUploadFailed, Legacy_MediaPlayer_PlaybackResumed, SKILL_PERMISSION_ACCEPTED, FitnessSessionController_FitnessSessionPaused, Legacy_AudioPlayer_PlaybackPaused, Alexa_Presentation_HTML_LifecycleStateChanged, LocalApplication_SipUserAgent_Event, Legacy_MediaPlayer_PlaybackStarted, REMINDER_STATUS_CHANGED, MessagingController_UploadConversations, ITEMS_DELETED, Legacy_AuxController_PluggedStateChanged, Legacy_AudioPlayer_PlaybackStarted, Alexa_FileManager_UploadController_UploadStarted, ITEMS_CREATED, Legacy_ExternalMediaPlayer_Event, LocalApplication_LocalMediaPlayer_Event, LocalApplication_KnightContacts_Event, LocalApplication_Calendar_Event, Legacy_AlertsController_DismissCommand, Legacy_AudioPlayer_PlaybackStutterFinished, Legacy_SpeechSynthesizer_SpeechFinished, Legacy_ExternalMediaPlayer_ReportDiscoveredPlayers, LocalApplication_SipClient_Event, Legacy_BluetoothNetwork_DeviceUnpairSuccess, Legacy_Speaker_VolumeChanged, CardRenderer_ReadContentFinished, LocalApplication_HomeAutomationMedia_Event, Legacy_BluetoothNetwork_CancelPairingMode, LocalApplication_DigitalDash_Event, CardRenderer_ReadContentStarted, Legacy_GameEngine_GameInputEvent, LocalApplication_LocalVoiceUI_Event, Legacy_Microphone_AudioRecording, LocalApplication_AlexaPlatformTestSpeechlet_Event, Legacy_HomeAutoWifiController_SsdpServiceDiscovered, Alexa_Camera_PhotoCaptureController_CancelCaptureFinished, Legacy_HomeAutoWifiController_DeviceReconnected, SKILL_ENABLED, Alexa_Camera_VideoCaptureController_CancelCaptureFinished, MessagingController_UpdateMessagesStatusRequest, REMINDER_STARTED, CustomInterfaceController_Expired, LocalApplication_AvaPhysicalShopping_Event, LocalApplication_WebVideoPlayer_Event, Legacy_HomeAutoWifiController_SsdpServiceTerminated, LocalApplication_FireflyShopping_Event, Legacy_PlaybackController_NextCommand, LocalApplication_Gallery_Event, Alexa_Presentation_PresentationDismissed, EffectsController_StateReceiptChangeRequest, LocalApplication_Alexa_Translation_LiveTranslation_Event, LocalApplication_AlexaNotifications_Event, REMINDER_DELETED, GameEngine_InputHandlerEvent, Legacy_PlaylistController_Response, LocalApplication_KnightHome_Event, Legacy_ListRenderer_ListItemEvent, AudioPlayer_PlaybackFailed, LocalApplication_KnightHomeThingsToTry_Event, Legacy_BluetoothNetwork_SetDeviceCategoriesFailed, Legacy_ExternalMediaPlayer_Logout, Alexa_FileManager_UploadController_UploadFinished, Legacy_ActivityManager_FocusChanged, Legacy_AlertsController_SnoozeCommand, Legacy_SpeechRecognizer_WakeWordChanged, Legacy_ListRenderer_GetListPageByToken, MessagingController_UpdateSendMessageStatusRequest, FitnessSessionController_FitnessSessionEnded, Alexa_Presentation_APL_RuntimeError, Legacy_ListRenderer_GetListPageByOrdinal, FitnessSessionController_FitnessSessionResumed, IN_SKILL_PRODUCT_SUBSCRIPTION_STARTED, Legacy_DeviceNotification_DeleteNotificationSucceeded, Legacy_SpeechSynthesizer_SpeechSynthesizerError, Alexa_Video_Xray_ShowDetailsFailed, Alexa_FileManager_UploadController_CancelUploadFinished, Legacy_SconeRemoteControl_PlayPause, Legacy_DeviceNotification_NotificationEnteredBackground, SKILL_PERMISSION_CHANGED, Legacy_AudioPlayer_Metadata, Legacy_AudioPlayer_PlaybackStutterStarted, AUDIO_ITEM_PLAYBACK_FINISHED, EffectsController_RequestGuiChangeRequest, FitnessSessionController_FitnessSessionStarted, Legacy_PlaybackController_LyricsViewedEvent, Legacy_ExternalMediaPlayer_Login, PlaybackController_PauseCommandIssued, Legacy_MediaPlayer_PlaybackIdle, Legacy_SconeRemoteControl_Previous, DeviceSetup_SetupCompleted, Legacy_MediaPlayer_PlaybackNearlyFinished, LocalApplication_todoRenderer_Event, Legacy_BluetoothNetwork_SetDeviceCategoriesSucceeded, Legacy_BluetoothNetwork_MediaControlSuccess, Legacy_HomeAutoWifiController_SsdpDiscoveryFinished, Alexa_Presentation_APL_LoadIndexListData, IN_SKILL_PRODUCT_SUBSCRIPTION_RENEWED, Legacy_BluetoothNetwork_MediaControlFailure, Legacy_AuxController_EnabledStateChanged, Legacy_FavoritesController_Response, Legacy_ListModel_ListStateUpdateRequest, Legacy_EqualizerController_EqualizerChanged, Legacy_MediaGrouping_GroupSyncEvent, Legacy_FavoritesController_Error, Legacy_ListModel_GetPageByTokenRequest, Legacy_ActivityManager_ActivityInterrupted, Legacy_MeetingClientController_Event, Legacy_Presentation_PresentationDismissedEvent, Legacy_Spotify_Event, Legacy_ExternalMediaPlayer_Error, Legacy_AuxController_DirectionChanged, AudioPlayer_PlaybackNearlyFinished, Alexa_Camera_PhotoCaptureController_CaptureFinished, Legacy_UDPController_BroadcastResponse, Legacy_AudioPlayer_PlaybackResumed, Legacy_DeviceNotification_DeleteNotificationFailed]
    """
    Legacy_AudioPlayerGui_LyricsViewedEvent = "Legacy.AudioPlayerGui.LyricsViewedEvent"
    Legacy_ListModel_DeleteItemRequest = "Legacy.ListModel.DeleteItemRequest"
    Legacy_MediaPlayer_SequenceModified = "Legacy.MediaPlayer.SequenceModified"
    Legacy_PlaybackController_ButtonCommand = "Legacy.PlaybackController.ButtonCommand"
    EffectsController_RequestEffectChangeRequest = "EffectsController.RequestEffectChangeRequest"
    Legacy_ExternalMediaPlayer_RequestToken = "Legacy.ExternalMediaPlayer.RequestToken"
    ITEMS_UPDATED = "ITEMS_UPDATED"
    Alexa_Video_Xray_ShowDetailsSuccessful = "Alexa.Video.Xray.ShowDetailsSuccessful"
    PlaybackController_NextCommandIssued = "PlaybackController.NextCommandIssued"
    Legacy_MediaPlayer_PlaybackFinished = "Legacy.MediaPlayer.PlaybackFinished"
    Alexa_Camera_VideoCaptureController_CaptureFailed = "Alexa.Camera.VideoCaptureController.CaptureFailed"
    SKILL_DISABLED = "SKILL_DISABLED"
    Alexa_Camera_VideoCaptureController_CancelCaptureFailed = "Alexa.Camera.VideoCaptureController.CancelCaptureFailed"
    CustomInterfaceController_EventsReceived = "CustomInterfaceController.EventsReceived"
    Legacy_DeviceNotification_NotificationStarted = "Legacy.DeviceNotification.NotificationStarted"
    REMINDER_UPDATED = "REMINDER_UPDATED"
    AUDIO_ITEM_PLAYBACK_STOPPED = "AUDIO_ITEM_PLAYBACK_STOPPED"
    Legacy_AuxController_InputActivityStateChanged = "Legacy.AuxController.InputActivityStateChanged"
    LocalApplication_MShopPurchasing_Event = "LocalApplication.MShopPurchasing.Event"
    Legacy_ExternalMediaPlayer_AuthorizationComplete = "Legacy.ExternalMediaPlayer.AuthorizationComplete"
    LocalApplication_HHOPhotos_Event = "LocalApplication.HHOPhotos.Event"
    Alexa_Presentation_APL_UserEvent = "Alexa.Presentation.APL.UserEvent"
    Legacy_AudioPlayer_PlaybackInterrupted = "Legacy.AudioPlayer.PlaybackInterrupted"
    Legacy_BluetoothNetwork_DeviceUnpairFailure = "Legacy.BluetoothNetwork.DeviceUnpairFailure"
    IN_SKILL_PRODUCT_SUBSCRIPTION_ENDED = "IN_SKILL_PRODUCT_SUBSCRIPTION_ENDED"
    Alexa_FileManager_UploadController_UploadFailed = "Alexa.FileManager.UploadController.UploadFailed"
    Legacy_BluetoothNetwork_DeviceConnectedFailure = "Legacy.BluetoothNetwork.DeviceConnectedFailure"
    Legacy_AudioPlayer_AudioStutter = "Legacy.AudioPlayer.AudioStutter"
    Alexa_Camera_VideoCaptureController_CaptureStarted = "Alexa.Camera.VideoCaptureController.CaptureStarted"
    Legacy_Speaker_MuteChanged = "Legacy.Speaker.MuteChanged"
    CardRenderer_DisplayContentFinished = "CardRenderer.DisplayContentFinished"
    Legacy_SpeechSynthesizer_SpeechStarted = "Legacy.SpeechSynthesizer.SpeechStarted"
    AudioPlayer_PlaybackStopped = "AudioPlayer.PlaybackStopped"
    Legacy_SoftwareUpdate_CheckSoftwareUpdateReport = "Legacy.SoftwareUpdate.CheckSoftwareUpdateReport"
    CardRenderer_DisplayContentStarted = "CardRenderer.DisplayContentStarted"
    LocalApplication_NotificationsApp_Event = "LocalApplication.NotificationsApp.Event"
    AudioPlayer_PlaybackStarted = "AudioPlayer.PlaybackStarted"
    Legacy_DeviceNotification_NotificationEnteredForground = "Legacy.DeviceNotification.NotificationEnteredForground"
    Legacy_DeviceNotification_SetNotificationFailed = "Legacy.DeviceNotification.SetNotificationFailed"
    Legacy_AudioPlayer_PeriodicPlaybackProgressReport = "Legacy.AudioPlayer.PeriodicPlaybackProgressReport"
    Legacy_HomeAutoWifiController_HttpNotified = "Legacy.HomeAutoWifiController.HttpNotified"
    Alexa_Camera_PhotoCaptureController_CancelCaptureFailed = "Alexa.Camera.PhotoCaptureController.CancelCaptureFailed"
    SKILL_ACCOUNT_LINKED = "SKILL_ACCOUNT_LINKED"
    LIST_UPDATED = "LIST_UPDATED"
    Legacy_DeviceNotification_NotificationSync = "Legacy.DeviceNotification.NotificationSync"
    Legacy_SconeRemoteControl_VolumeDown = "Legacy.SconeRemoteControl.VolumeDown"
    Legacy_MediaPlayer_PlaybackPaused = "Legacy.MediaPlayer.PlaybackPaused"
    Legacy_Presentation_PresentationUserEvent = "Legacy.Presentation.PresentationUserEvent"
    PlaybackController_PlayCommandIssued = "PlaybackController.PlayCommandIssued"
    Legacy_ListModel_UpdateItemRequest = "Legacy.ListModel.UpdateItemRequest"
    Messaging_MessageReceived = "Messaging.MessageReceived"
    Legacy_SoftwareUpdate_InitiateSoftwareUpdateReport = "Legacy.SoftwareUpdate.InitiateSoftwareUpdateReport"
    AUDIO_ITEM_PLAYBACK_FAILED = "AUDIO_ITEM_PLAYBACK_FAILED"
    LocalApplication_DeviceMessaging_Event = "LocalApplication.DeviceMessaging.Event"
    Alexa_Camera_PhotoCaptureController_CaptureFailed = "Alexa.Camera.PhotoCaptureController.CaptureFailed"
    Legacy_AudioPlayer_PlaybackIdle = "Legacy.AudioPlayer.PlaybackIdle"
    Legacy_BluetoothNetwork_EnterPairingModeSuccess = "Legacy.BluetoothNetwork.EnterPairingModeSuccess"
    Legacy_AudioPlayer_PlaybackError = "Legacy.AudioPlayer.PlaybackError"
    Legacy_ListModel_GetPageByOrdinalRequest = "Legacy.ListModel.GetPageByOrdinalRequest"
    Legacy_MediaGrouping_GroupChangeResponseEvent = "Legacy.MediaGrouping.GroupChangeResponseEvent"
    Legacy_BluetoothNetwork_DeviceDisconnectedFailure = "Legacy.BluetoothNetwork.DeviceDisconnectedFailure"
    Legacy_BluetoothNetwork_EnterPairingModeFailure = "Legacy.BluetoothNetwork.EnterPairingModeFailure"
    Legacy_SpeechSynthesizer_SpeechInterrupted = "Legacy.SpeechSynthesizer.SpeechInterrupted"
    PlaybackController_PreviousCommandIssued = "PlaybackController.PreviousCommandIssued"
    Legacy_AudioPlayer_PlaybackFinished = "Legacy.AudioPlayer.PlaybackFinished"
    Legacy_System_UserInactivity = "Legacy.System.UserInactivity"
    Display_UserEvent = "Display.UserEvent"
    Legacy_PhoneCallController_Event = "Legacy.PhoneCallController.Event"
    Legacy_DeviceNotification_SetNotificationSucceeded = "Legacy.DeviceNotification.SetNotificationSucceeded"
    LocalApplication_Photos_Event = "LocalApplication.Photos.Event"
    LocalApplication_VideoExperienceService_Event = "LocalApplication.VideoExperienceService.Event"
    Legacy_ContentManager_ContentPlaybackTerminated = "Legacy.ContentManager.ContentPlaybackTerminated"
    Legacy_PlaybackController_PlayCommand = "Legacy.PlaybackController.PlayCommand"
    Legacy_PlaylistController_ErrorResponse = "Legacy.PlaylistController.ErrorResponse"
    Legacy_SconeRemoteControl_VolumeUp = "Legacy.SconeRemoteControl.VolumeUp"
    MessagingController_UpdateConversationsStatus = "MessagingController.UpdateConversationsStatus"
    Legacy_BluetoothNetwork_DeviceDisconnectedSuccess = "Legacy.BluetoothNetwork.DeviceDisconnectedSuccess"
    LocalApplication_Communications_Event = "LocalApplication.Communications.Event"
    AUDIO_ITEM_PLAYBACK_STARTED = "AUDIO_ITEM_PLAYBACK_STARTED"
    Legacy_BluetoothNetwork_DevicePairFailure = "Legacy.BluetoothNetwork.DevicePairFailure"
    LIST_DELETED = "LIST_DELETED"
    Legacy_PlaybackController_ToggleCommand = "Legacy.PlaybackController.ToggleCommand"
    Legacy_BluetoothNetwork_DevicePairSuccess = "Legacy.BluetoothNetwork.DevicePairSuccess"
    Legacy_MediaPlayer_PlaybackError = "Legacy.MediaPlayer.PlaybackError"
    AudioPlayer_PlaybackFinished = "AudioPlayer.PlaybackFinished"
    Legacy_DeviceNotification_NotificationStopped = "Legacy.DeviceNotification.NotificationStopped"
    Legacy_SipClient_Event = "Legacy.SipClient.Event"
    Display_ElementSelected = "Display.ElementSelected"
    LocalApplication_MShop_Event = "LocalApplication.MShop.Event"
    Legacy_ListModel_AddItemRequest = "Legacy.ListModel.AddItemRequest"
    Legacy_BluetoothNetwork_ScanDevicesReport = "Legacy.BluetoothNetwork.ScanDevicesReport"
    Legacy_MediaPlayer_PlaybackStopped = "Legacy.MediaPlayer.PlaybackStopped"
    Legacy_AudioPlayerGui_ButtonClickedEvent = "Legacy.AudioPlayerGui.ButtonClickedEvent"
    LocalApplication_AlexaVoiceLayer_Event = "LocalApplication.AlexaVoiceLayer.Event"
    Legacy_PlaybackController_PreviousCommand = "Legacy.PlaybackController.PreviousCommand"
    Legacy_AudioPlayer_InitialPlaybackProgressReport = "Legacy.AudioPlayer.InitialPlaybackProgressReport"
    Legacy_BluetoothNetwork_DeviceConnectedSuccess = "Legacy.BluetoothNetwork.DeviceConnectedSuccess"
    LIST_CREATED = "LIST_CREATED"
    Legacy_ActivityManager_ActivityContextRemovedEvent = "Legacy.ActivityManager.ActivityContextRemovedEvent"
    ALL_LISTS_CHANGED = "ALL_LISTS_CHANGED"
    Legacy_AudioPlayer_PlaybackNearlyFinished = "Legacy.AudioPlayer.PlaybackNearlyFinished"
    Legacy_MediaGrouping_GroupChangeNotificationEvent = "Legacy.MediaGrouping.GroupChangeNotificationEvent"
    LocalApplication_Sentry_Event = "LocalApplication.Sentry.Event"
    SKILL_PROACTIVE_SUBSCRIPTION_CHANGED = "SKILL_PROACTIVE_SUBSCRIPTION_CHANGED"
    REMINDER_CREATED = "REMINDER_CREATED"
    Alexa_Presentation_HTML_Event = "Alexa.Presentation.HTML.Event"
    FitnessSessionController_FitnessSessionError = "FitnessSessionController.FitnessSessionError"
    Legacy_SconeRemoteControl_Next = "Legacy.SconeRemoteControl.Next"
    Alexa_Camera_VideoCaptureController_CaptureFinished = "Alexa.Camera.VideoCaptureController.CaptureFinished"
    Legacy_MediaPlayer_SequenceItemsRequested = "Legacy.MediaPlayer.SequenceItemsRequested"
    Legacy_PlaybackController_PauseCommand = "Legacy.PlaybackController.PauseCommand"
    LocalApplication_AlexaVision_Event = "LocalApplication.AlexaVision.Event"
    LocalApplication_Closet_Event = "LocalApplication.Closet.Event"
    Alexa_FileManager_UploadController_CancelUploadFailed = "Alexa.FileManager.UploadController.CancelUploadFailed"
    Legacy_MediaPlayer_PlaybackResumed = "Legacy.MediaPlayer.PlaybackResumed"
    SKILL_PERMISSION_ACCEPTED = "SKILL_PERMISSION_ACCEPTED"
    FitnessSessionController_FitnessSessionPaused = "FitnessSessionController.FitnessSessionPaused"
    Legacy_AudioPlayer_PlaybackPaused = "Legacy.AudioPlayer.PlaybackPaused"
    Alexa_Presentation_HTML_LifecycleStateChanged = "Alexa.Presentation.HTML.LifecycleStateChanged"
    LocalApplication_SipUserAgent_Event = "LocalApplication.SipUserAgent.Event"
    Legacy_MediaPlayer_PlaybackStarted = "Legacy.MediaPlayer.PlaybackStarted"
    REMINDER_STATUS_CHANGED = "REMINDER_STATUS_CHANGED"
    MessagingController_UploadConversations = "MessagingController.UploadConversations"
    ITEMS_DELETED = "ITEMS_DELETED"
    Legacy_AuxController_PluggedStateChanged = "Legacy.AuxController.PluggedStateChanged"
    Legacy_AudioPlayer_PlaybackStarted = "Legacy.AudioPlayer.PlaybackStarted"
    Alexa_FileManager_UploadController_UploadStarted = "Alexa.FileManager.UploadController.UploadStarted"
    ITEMS_CREATED = "ITEMS_CREATED"
    Legacy_ExternalMediaPlayer_Event = "Legacy.ExternalMediaPlayer.Event"
    LocalApplication_LocalMediaPlayer_Event = "LocalApplication.LocalMediaPlayer.Event"
    LocalApplication_KnightContacts_Event = "LocalApplication.KnightContacts.Event"
    LocalApplication_Calendar_Event = "LocalApplication.Calendar.Event"
    Legacy_AlertsController_DismissCommand = "Legacy.AlertsController.DismissCommand"
    Legacy_AudioPlayer_PlaybackStutterFinished = "Legacy.AudioPlayer.PlaybackStutterFinished"
    Legacy_SpeechSynthesizer_SpeechFinished = "Legacy.SpeechSynthesizer.SpeechFinished"
    Legacy_ExternalMediaPlayer_ReportDiscoveredPlayers = "Legacy.ExternalMediaPlayer.ReportDiscoveredPlayers"
    LocalApplication_SipClient_Event = "LocalApplication.SipClient.Event"
    Legacy_BluetoothNetwork_DeviceUnpairSuccess = "Legacy.BluetoothNetwork.DeviceUnpairSuccess"
    Legacy_Speaker_VolumeChanged = "Legacy.Speaker.VolumeChanged"
    CardRenderer_ReadContentFinished = "CardRenderer.ReadContentFinished"
    LocalApplication_HomeAutomationMedia_Event = "LocalApplication.HomeAutomationMedia.Event"
    Legacy_BluetoothNetwork_CancelPairingMode = "Legacy.BluetoothNetwork.CancelPairingMode"
    LocalApplication_DigitalDash_Event = "LocalApplication.DigitalDash.Event"
    CardRenderer_ReadContentStarted = "CardRenderer.ReadContentStarted"
    Legacy_GameEngine_GameInputEvent = "Legacy.GameEngine.GameInputEvent"
    LocalApplication_LocalVoiceUI_Event = "LocalApplication.LocalVoiceUI.Event"
    Legacy_Microphone_AudioRecording = "Legacy.Microphone.AudioRecording"
    LocalApplication_AlexaPlatformTestSpeechlet_Event = "LocalApplication.AlexaPlatformTestSpeechlet.Event"
    Legacy_HomeAutoWifiController_SsdpServiceDiscovered = "Legacy.HomeAutoWifiController.SsdpServiceDiscovered"
    Alexa_Camera_PhotoCaptureController_CancelCaptureFinished = "Alexa.Camera.PhotoCaptureController.CancelCaptureFinished"
    Legacy_HomeAutoWifiController_DeviceReconnected = "Legacy.HomeAutoWifiController.DeviceReconnected"
    SKILL_ENABLED = "SKILL_ENABLED"
    Alexa_Camera_VideoCaptureController_CancelCaptureFinished = "Alexa.Camera.VideoCaptureController.CancelCaptureFinished"
    MessagingController_UpdateMessagesStatusRequest = "MessagingController.UpdateMessagesStatusRequest"
    REMINDER_STARTED = "REMINDER_STARTED"
    CustomInterfaceController_Expired = "CustomInterfaceController.Expired"
    LocalApplication_AvaPhysicalShopping_Event = "LocalApplication.AvaPhysicalShopping.Event"
    LocalApplication_WebVideoPlayer_Event = "LocalApplication.WebVideoPlayer.Event"
    Legacy_HomeAutoWifiController_SsdpServiceTerminated = "Legacy.HomeAutoWifiController.SsdpServiceTerminated"
    LocalApplication_FireflyShopping_Event = "LocalApplication.FireflyShopping.Event"
    Legacy_PlaybackController_NextCommand = "Legacy.PlaybackController.NextCommand"
    LocalApplication_Gallery_Event = "LocalApplication.Gallery.Event"
    Alexa_Presentation_PresentationDismissed = "Alexa.Presentation.PresentationDismissed"
    EffectsController_StateReceiptChangeRequest = "EffectsController.StateReceiptChangeRequest"
    LocalApplication_Alexa_Translation_LiveTranslation_Event = "LocalApplication.Alexa.Translation.LiveTranslation.Event"
    LocalApplication_AlexaNotifications_Event = "LocalApplication.AlexaNotifications.Event"
    REMINDER_DELETED = "REMINDER_DELETED"
    GameEngine_InputHandlerEvent = "GameEngine.InputHandlerEvent"
    Legacy_PlaylistController_Response = "Legacy.PlaylistController.Response"
    LocalApplication_KnightHome_Event = "LocalApplication.KnightHome.Event"
    Legacy_ListRenderer_ListItemEvent = "Legacy.ListRenderer.ListItemEvent"
    AudioPlayer_PlaybackFailed = "AudioPlayer.PlaybackFailed"
    LocalApplication_KnightHomeThingsToTry_Event = "LocalApplication.KnightHomeThingsToTry.Event"
    Legacy_BluetoothNetwork_SetDeviceCategoriesFailed = "Legacy.BluetoothNetwork.SetDeviceCategoriesFailed"
    Legacy_ExternalMediaPlayer_Logout = "Legacy.ExternalMediaPlayer.Logout"
    Alexa_FileManager_UploadController_UploadFinished = "Alexa.FileManager.UploadController.UploadFinished"
    Legacy_ActivityManager_FocusChanged = "Legacy.ActivityManager.FocusChanged"
    Legacy_AlertsController_SnoozeCommand = "Legacy.AlertsController.SnoozeCommand"
    Legacy_SpeechRecognizer_WakeWordChanged = "Legacy.SpeechRecognizer.WakeWordChanged"
    Legacy_ListRenderer_GetListPageByToken = "Legacy.ListRenderer.GetListPageByToken"
    MessagingController_UpdateSendMessageStatusRequest = "MessagingController.UpdateSendMessageStatusRequest"
    FitnessSessionController_FitnessSessionEnded = "FitnessSessionController.FitnessSessionEnded"
    Alexa_Presentation_APL_RuntimeError = "Alexa.Presentation.APL.RuntimeError"
    Legacy_ListRenderer_GetListPageByOrdinal = "Legacy.ListRenderer.GetListPageByOrdinal"
    FitnessSessionController_FitnessSessionResumed = "FitnessSessionController.FitnessSessionResumed"
    IN_SKILL_PRODUCT_SUBSCRIPTION_STARTED = "IN_SKILL_PRODUCT_SUBSCRIPTION_STARTED"
    Legacy_DeviceNotification_DeleteNotificationSucceeded = "Legacy.DeviceNotification.DeleteNotificationSucceeded"
    Legacy_SpeechSynthesizer_SpeechSynthesizerError = "Legacy.SpeechSynthesizer.SpeechSynthesizerError"
    Alexa_Video_Xray_ShowDetailsFailed = "Alexa.Video.Xray.ShowDetailsFailed"
    Alexa_FileManager_UploadController_CancelUploadFinished = "Alexa.FileManager.UploadController.CancelUploadFinished"
    Legacy_SconeRemoteControl_PlayPause = "Legacy.SconeRemoteControl.PlayPause"
    Legacy_DeviceNotification_NotificationEnteredBackground = "Legacy.DeviceNotification.NotificationEnteredBackground"
    SKILL_PERMISSION_CHANGED = "SKILL_PERMISSION_CHANGED"
    Legacy_AudioPlayer_Metadata = "Legacy.AudioPlayer.Metadata"
    Legacy_AudioPlayer_PlaybackStutterStarted = "Legacy.AudioPlayer.PlaybackStutterStarted"
    AUDIO_ITEM_PLAYBACK_FINISHED = "AUDIO_ITEM_PLAYBACK_FINISHED"
    EffectsController_RequestGuiChangeRequest = "EffectsController.RequestGuiChangeRequest"
    FitnessSessionController_FitnessSessionStarted = "FitnessSessionController.FitnessSessionStarted"
    Legacy_PlaybackController_LyricsViewedEvent = "Legacy.PlaybackController.LyricsViewedEvent"
    Legacy_ExternalMediaPlayer_Login = "Legacy.ExternalMediaPlayer.Login"
    PlaybackController_PauseCommandIssued = "PlaybackController.PauseCommandIssued"
    Legacy_MediaPlayer_PlaybackIdle = "Legacy.MediaPlayer.PlaybackIdle"
    Legacy_SconeRemoteControl_Previous = "Legacy.SconeRemoteControl.Previous"
    DeviceSetup_SetupCompleted = "DeviceSetup.SetupCompleted"
    Legacy_MediaPlayer_PlaybackNearlyFinished = "Legacy.MediaPlayer.PlaybackNearlyFinished"
    LocalApplication_todoRenderer_Event = "LocalApplication.todoRenderer.Event"
    Legacy_BluetoothNetwork_SetDeviceCategoriesSucceeded = "Legacy.BluetoothNetwork.SetDeviceCategoriesSucceeded"
    Legacy_BluetoothNetwork_MediaControlSuccess = "Legacy.BluetoothNetwork.MediaControlSuccess"
    Legacy_HomeAutoWifiController_SsdpDiscoveryFinished = "Legacy.HomeAutoWifiController.SsdpDiscoveryFinished"
    Alexa_Presentation_APL_LoadIndexListData = "Alexa.Presentation.APL.LoadIndexListData"
    IN_SKILL_PRODUCT_SUBSCRIPTION_RENEWED = "IN_SKILL_PRODUCT_SUBSCRIPTION_RENEWED"
    Legacy_BluetoothNetwork_MediaControlFailure = "Legacy.BluetoothNetwork.MediaControlFailure"
    Legacy_AuxController_EnabledStateChanged = "Legacy.AuxController.EnabledStateChanged"
    Legacy_FavoritesController_Response = "Legacy.FavoritesController.Response"
    Legacy_ListModel_ListStateUpdateRequest = "Legacy.ListModel.ListStateUpdateRequest"
    Legacy_EqualizerController_EqualizerChanged = "Legacy.EqualizerController.EqualizerChanged"
    Legacy_MediaGrouping_GroupSyncEvent = "Legacy.MediaGrouping.GroupSyncEvent"
    Legacy_FavoritesController_Error = "Legacy.FavoritesController.Error"
    Legacy_ListModel_GetPageByTokenRequest = "Legacy.ListModel.GetPageByTokenRequest"
    Legacy_ActivityManager_ActivityInterrupted = "Legacy.ActivityManager.ActivityInterrupted"
    Legacy_MeetingClientController_Event = "Legacy.MeetingClientController.Event"
    Legacy_Presentation_PresentationDismissedEvent = "Legacy.Presentation.PresentationDismissedEvent"
    Legacy_Spotify_Event = "Legacy.Spotify.Event"
    Legacy_ExternalMediaPlayer_Error = "Legacy.ExternalMediaPlayer.Error"
    Legacy_AuxController_DirectionChanged = "Legacy.AuxController.DirectionChanged"
    AudioPlayer_PlaybackNearlyFinished = "AudioPlayer.PlaybackNearlyFinished"
    Alexa_Camera_PhotoCaptureController_CaptureFinished = "Alexa.Camera.PhotoCaptureController.CaptureFinished"
    Legacy_UDPController_BroadcastResponse = "Legacy.UDPController.BroadcastResponse"
    Legacy_AudioPlayer_PlaybackResumed = "Legacy.AudioPlayer.PlaybackResumed"
    Legacy_DeviceNotification_DeleteNotificationFailed = "Legacy.DeviceNotification.DeleteNotificationFailed"

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Returns the model properties as a dict"""
        result = {self.name: self.value}
        return result

    def to_str(self):
        # type: () -> str
        """Returns the string representation of the model"""
        return pprint.pformat(self.value)

    def __repr__(self):
        # type: () -> str
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        # type: (Any) -> bool
        """Returns true if both objects are equal"""
        if not isinstance(other, EventNameType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (Any) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
