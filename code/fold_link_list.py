"""
将一个链表对折，比如给定的是偶数长度的1->2->3->4->5->6的链表，对折之后是3->2->1->6->5->4， 如果给定的是奇数长度的1->2->3->4->5->6->7，对折之后是3->2->1->4->7->6->5
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        tmp = self
        res = []
        while tmp:
            res.append(str(tmp.val))
            tmp = tmp.next

        return "->".join(res)

def reverse(head):
    pre = None
    cur = head
    while cur:
        next = cur.next
        cur.next = pre
        pre = cur
        cur = next

    return pre


def fold_linked_list(head):
    if not head or not head.next:
        return head  # 链表为空或只有一个元素，直接返回

    # 快慢指针找中点
    slow, fast = head, head
    prev_slow = None  # 记录慢指针前一个节点，用于切断后半部分链表
    while fast and fast.next:
        prev_slow = slow
        slow = slow.next
        fast = fast.next.next

    # 切断链表，准备反转后半部分
    odd = False
    if fast:  # 奇数长度时，slow在中间节点，fast已经越过了中间节点
        prev_slow = slow
        slow = slow.next
        odd = True
    prev_slow.next = None  # 断开链表

    # 分别翻转
    slow = reverse(slow)
    head = reverse(head)

    mid = None
    if odd:
        mid = head
        head = head.next
        mid.next = None

    tail = head
    while tail.next:
        tail = tail.next

    if mid:
        tail.next = mid
        mid.next = slow
    else:
        tail.next = slow


    return head



if __name__ == "__main__":
    # 测试代码
    # 创建链表 1->2->3->4->5->6
    head = dummy_head = ListNode()
    for i in range(1, 8):
        head.next = ListNode(i)
        head = head.next
    print(dummy_head.next)
    folded_head = fold_linked_list(dummy_head.next)
    print(folded_head)
