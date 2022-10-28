#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

typedef struct node{
    char* name;
    struct node* xor_value;
} Node;

// prototypes
void insert_string(Node** head, const char* newObj);
int insert_before(Node** head, const char* before, const char* newObj);
int insert_after(Node** head, const char* after, const char* newObj);
int remove_string(Node** head, char* result);
int remove_after(Node** head, const char *after, char *result);
int remove_before(Node** head, const char *before, char *result);
void free_all(Node** head);
void printList(Node** head);


Node* calculate_xor_value(Node* before, Node* after){
  return (Node*)((__intptr_t)before ^ (__intptr_t)after);
}


// Inserts the string at the beginning of the XOR linked list.
void insert_string(Node** head, const char* newObj){
	
	// create new node to use as head
	Node *new_head = (Node*)malloc(sizeof(char*) + sizeof(Node*));
	// copy the new name so we can free it later
	char* new_name = (char*)malloc(sizeof(char*)*strlen(newObj)+1);
	strcpy(new_name, newObj);
    new_head->name = new_name;
	new_head->xor_value = calculate_xor_value(NULL, *head); // prev is null, next is the old head

	// if the linked list is not empty we need to recalculate the xor value of the first element
	if(*head != NULL){
		(*head)->xor_value = calculate_xor_value(new_head, calculate_xor_value(NULL, (*head)->xor_value));
	}

	// change the old head to the new head
    *head = new_head; 
}


// If possible, inserts before the string "before" and returns true. Returns 
// false if not possible (e.g., the before string is not in the list)
int insert_before(Node** head, const char* before, const char* newObj){
	// empty list
	if(*head == NULL){
		return false;
	}
	// if we want to insert a new head
	if(!strcmp((*head)->name, before)){
		insert_string(head, newObj);
		return true;
	}

	Node *prev = NULL;
	Node *curr = *head;

	// denotes whether the string "before" has been found, allowing the insertion to occur
	bool flag = false; 

	// iterate through the nodes in the linked list
	while(curr != NULL){
		if(!strcmp(curr->name, before)){
			flag = true;

			// create the new node
			Node *new_node = (Node*)malloc(sizeof(char*) + sizeof(Node*));
			new_node->xor_value = calculate_xor_value(prev, curr);
			char* new_name = (char*)malloc(sizeof(char*)*strlen(newObj)+1);
			strcpy(new_name, newObj);
  		    new_node->name = new_name;

			// change xor values of nodes before and after the new node
			Node *tmp = prev;
			prev->xor_value = calculate_xor_value(calculate_xor_value(prev->xor_value, curr), new_node);
			curr->xor_value = calculate_xor_value(new_node, calculate_xor_value(curr->xor_value, tmp));
			
			break;
		}

		// keep iterating
		Node *temp = prev;
		prev = curr;
		curr = calculate_xor_value(temp, prev->xor_value);
	}

	return flag;
}


// If possible, inserts after the string "after" and returns true. Returns false if
// not possible (e.g., the after string is not in the list)
int insert_after(Node** head, const char* after, const char* newObj){
	// empty list
	if(*head == NULL){
		return false;
	}

	Node *prev = NULL;
	Node *curr = *head;

	// iterate through the list
	while(curr != NULL){
		Node *temp = prev;
		prev = curr;
		curr = calculate_xor_value(temp, prev->xor_value);
	}

	Node *tail = prev;
	// pass in the tail as the head
	int x = insert_before(&tail, after, newObj);

  return x;
}


// If possible removes the string at the beginning of the XOR Linked list and returns
// its value in result. If the removal is successful, it returns true, otherwise it returns
// false
int remove_string(Node** head, char* result){
		if(*head == NULL){
			return false;
		}
		else{
			strcpy(result, (*head)->name);

			// get the second node
			Node *second_node = calculate_xor_value((*head)->xor_value, NULL);
			// change its xor value now that head is removed
			second_node->xor_value = calculate_xor_value(second_node->xor_value, *head);

			free((*head)->name);
			free(*head);
			*head = second_node;
		}
	
  return true;
}


// If possible, removes the string before the string "before" and fills in the
// result buffer with its value. If the removal is successful it returns true,
// otherwise it returns false
int remove_before(Node** head, const char *before, char *result){
	// empty list
	if(*head == NULL){
		return false;
	}
	// if we want to remove before the head
	if(!strcmp((*head)->name, before)){
		return false;
	}

	// find the second node
	Node *node2 = calculate_xor_value((*head)->xor_value, NULL);
	// if we are trying to remove the head:
	if(!strcmp(node2->name, before)){
		remove_string(head, result);
		return true;
	}

	Node *prev = NULL;
	Node *curr = *head;

	// denotes whether the string "before" has been found
	bool flag = false; 

	// iterate through the nodes in the linked list
	while(curr != NULL){
		
		if(!strcmp(curr->name, before)){
			flag = true;

			// return the name of the removed node
			strcpy(result, curr->name);
			
			// change the xor value of the node previous to the one we want to remove
			Node *prev_prev = calculate_xor_value(prev->xor_value, curr);
			prev_prev->xor_value = calculate_xor_value(calculate_xor_value(prev_prev->xor_value, prev), curr);
			
			// change the xor value of the node after the one we want to remove
			curr->xor_value = calculate_xor_value(calculate_xor_value(prev->xor_value, curr), calculate_xor_value(curr->xor_value, prev));

			// free memory of removed node
			free(prev->name);
			free(prev);
			break;
		}
		
		Node *temp = prev;
		prev = curr;
		curr = calculate_xor_value(temp, prev->xor_value);
	}
	
	return flag;
}


// If possible, removes the string after the string "after" and fills in the result
//buffer with its value. If successful return true, otherwise returns false
int remove_after(Node** head, const char *after, char *result){
	// empty list
	if(*head == NULL){
		return false;
	}
	
    Node *prev = NULL;
	Node *curr = *head;

	// iterate through the list
	while(curr != NULL){
		Node *temp = prev;
		prev = curr;
		curr = calculate_xor_value(temp, prev->xor_value);
	}

	Node *tail = prev;
	int result = remove_before(&tail, after, result);

    return result;
}


// Removes all nodes and releases any memory allocated to the linked list
void free_all(Node** head){
    Node *prev = NULL;
	Node *curr = *head;

	// iterate through the list
	while(curr != NULL){
		Node *temp = prev;
		prev = curr;
		curr = calculate_xor_value(temp, prev->xor_value);

		// free memory
		free(prev->name);
		free(prev);
	}
}


// Prints out a human-readable representation of a xor linked list 
void printList(Node** head)
{
    // Stores XOR pointer
    // in current node
    Node* curr = *head;
 
    // Stores XOR pointer of
    // in previous Node
    Node* prev = NULL;
 
    // Stores XOR pointer of
    // in next node
    Node* next;
 
    // Traverse XOR linked list
    while (curr != NULL) {
 
        // Print current node
        printf("%s ", curr->name);
 
        // Forward traversal
        next = calculate_xor_value(prev, curr->xor_value);
 
        // Update prev
        prev = curr;
 
        // Update curr
        curr = next;
    }
}