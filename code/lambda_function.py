# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
# Licensed under the MIT License. See the LICENSE accompanying this file
# for the specific language governing permissions and limitations under
# the License.

import boto3
import json
import email


def lambda_handler(event, context):
    try:
        # first code will fetch fromaddress, subject and messageId
        # then it will call workmail API to fetch actual message using this messageId
        # and then it will parse the message properly to convert it into text message

        workmail = boto3.client('workmailmessageflow', region_name=<YOUR REGION HERE>)
        
        
        from_addr = event['envelope']['mailFrom']['address']
        subject = event['subject']
        flowDirection = event['flowDirection']
        msg_id = event['messageId']
        
        # calling workmail API to fetch message body
        raw_msg = workmail.get_raw_message_content(messageId=msg_id)
        t = raw_msg['messageContent'].read()
        parsed_msg = email.message_from_bytes(t)
        
        if parsed_msg.is_multipart():
            for part in parsed_msg.walk():
                payload = part.get_payload(decode=True) #returns a bytes object
                if type(payload) is bytes:
                    msg_text = payload.decode('utf-8') #utf-8 is default
                    print('*** Multipart payload ****', msg_text)
                    break
        else:
            payload = parsed_msg.get_payload(decode=True)
            if type(payload) is bytes:
                msg_text = payload.decode('utf-8') #utf-8 is default
                print('*** Single payload ****', msg_text)
        

    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(e)
        raise e

    # Return value is ignored when Lambda is configured asynchronously at Amazon WorkMail
    # For more information, see https://docs.aws.amazon.com/workmail/latest/adminguide/lambda.html
    return {
          'actions': [
          {
            'allRecipients': True,                  # For all recipients
            'action' : { 'type' : 'DEFAULT' }       # let the email be sent normally
          }
        ]}
