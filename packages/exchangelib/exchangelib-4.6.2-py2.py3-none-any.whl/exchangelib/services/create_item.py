from collections import OrderedDict

from .common import EWSAccountService
from ..util import create_element, set_xml_value, MNS


class CreateItem(EWSAccountService):
    """Take a folder and a list of items. Return the result of creation as a list of tuples (success[True|False],
    errormessage), in the same order as the input list.

    MSDN: https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/createitem-operation
    """

    SERVICE_NAME = 'CreateItem'
    element_container_name = '{%s}Items' % MNS

    def call(self, items, folder, message_disposition, send_meeting_invitations):
        from ..folders import BaseFolder, FolderId
        from ..items import SAVE_ONLY, SEND_AND_SAVE_COPY, SEND_ONLY, \
            SEND_MEETING_INVITATIONS_CHOICES, MESSAGE_DISPOSITION_CHOICES
        if message_disposition not in MESSAGE_DISPOSITION_CHOICES:
            raise ValueError("'message_disposition' %s must be one of %s" % (
                message_disposition, MESSAGE_DISPOSITION_CHOICES
            ))
        if send_meeting_invitations not in SEND_MEETING_INVITATIONS_CHOICES:
            raise ValueError("'send_meeting_invitations' %s must be one of %s" % (
                send_meeting_invitations, SEND_MEETING_INVITATIONS_CHOICES
            ))
        if folder is not None:
            if not isinstance(folder, (BaseFolder, FolderId)):
                raise ValueError("'folder' %r must be a Folder or FolderId instance" % folder)
            if folder.account != self.account:
                raise ValueError('"Folder must belong to this account')
        if message_disposition == SAVE_ONLY and folder is None:
            raise AttributeError("Folder must be supplied when in save-only mode")
        if message_disposition == SEND_AND_SAVE_COPY and folder is None:
            folder = self.account.sent  # 'Sent' is default EWS behaviour
        if message_disposition == SEND_ONLY and folder is not None:
            raise AttributeError("Folder must be None in send-ony mode")
        return self._elems_to_objs(self._chunked_get_elements(
            self.get_payload,
            items=items,
            folder=folder,
            message_disposition=message_disposition,
            send_meeting_invitations=send_meeting_invitations,
        ))

    def _elems_to_objs(self, elems):
        from ..items import BulkCreateResult
        for elem in elems:
            if isinstance(elem, (Exception, type(None))):
                yield elem
                continue
            if isinstance(elem, bool):
                yield elem
                continue
            yield BulkCreateResult.from_xml(elem=elem, account=self.account)

    @classmethod
    def _get_elements_in_container(cls, container):
        res = super()._get_elements_in_container(container)
        return res or [True]

    def get_payload(self, items, folder, message_disposition, send_meeting_invitations):
        """Take a list of Item objects (CalendarItem, Message etc) and return the XML for a CreateItem request.
        convert items to XML Elements.

        MessageDisposition is only applicable to email messages, where it is required.

        SendMeetingInvitations is required for calendar items. It is also applicable to tasks, meeting request
        responses (see
        https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/createitem-operation-meeting-request
        ) and sharing
        invitation accepts (see
        https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/createitem-acceptsharinginvitation
        ). The last two are not supported yet.

        :param items:
        :param folder:
        :param message_disposition:
        :param send_meeting_invitations:
        """
        createitem = create_element(
            'm:%s' % self.SERVICE_NAME,
            attrs=OrderedDict([
                ('MessageDisposition', message_disposition),
                ('SendMeetingInvitations', send_meeting_invitations),
            ])
        )
        if folder:
            saveditemfolderid = create_element('m:SavedItemFolderId')
            set_xml_value(saveditemfolderid, folder, version=self.account.version)
            createitem.append(saveditemfolderid)
        item_elems = create_element('m:Items')
        for item in items:
            if not item.account:
                item.account = self.account
            set_xml_value(item_elems, item, version=self.account.version)
        if not len(item_elems):
            raise ValueError('"items" must not be empty')
        createitem.append(item_elems)
        return createitem
