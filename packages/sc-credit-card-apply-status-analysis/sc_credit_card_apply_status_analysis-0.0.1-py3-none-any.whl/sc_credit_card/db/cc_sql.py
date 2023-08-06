#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
CHECK_BATCH_STATUS = """
SELECT batch_type, batch_status, batch_date, remarks
FROM cc_batch_status WHERE batch_type = %s
"""

INSERT_BATCH_STATUS = """
INSERT INTO cc_batch_status (batch_type, batch_status, batch_date, remarks)
VALUES (%s, %s, %s, %s);
"""

UPDATE_BATCH_STATUS = """
UPDATE cc_batch_status SET 
    batch_status = %s,
    batch_date = %s, 
    remarks = %s, 
    update_time = NOW()
where batch_type = %s
"""

TRUNCATE_APPLY_STATUS = """
TRUNCATE TABLE cc_appr_status
"""

CHECK_APPLY_STATUS = """
SELECT apply_no, apply_date, apply_status, reject_reason
FROM cc_appr_status WHERE apply_no = %s
"""

INSERT_APPLY_STATUS = """
INSERT INTO cc_appr_status (
    apply_no, apply_date, card_type, card_no, manager_no, 
    manager_name, branch, sub_branch, apply_status, reject_reason, 
    client_name, client_id_no, update_time
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW());
"""

UPDATE_APPLY_STATUS = """
UPDATE cc_appr_status SET 
    card_no = %s,
    apply_status = %s, 
    reject_reason = %s, 
    update_time = NOW()
where apply_no = %s
"""
