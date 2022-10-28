class SortedLinkedList implements SortedList{

	// first node
	private Node firstNode = null;
	// order: alphetical = 0
	//        reverse = 1
	private int order = 0;


    @Override
	public int size(){
		// get the head
		Node currNode = this.getFirst();
		// if the head is null, the list is empty
		if(currNode == null){
			return 0;
		}
		else{
			// there is at least one node
			int count = 1;
			// while there is a next node, get it
			while(currNode.getNext() != null){
				currNode = currNode.getNext();
				count++;
			}
			return count;
		}
	}


    @Override
	public void add(String string){
		Node node = new Node(string);
		this.add(node);
	}
	

    @Override
	public void add(Node node){
        // do not add duplicates
        if(this.isPresent(node.getString())){return;}
		if(!node.getString().matches("[a-zA-Z]+")){return;}

        Node currNode = this.getFirst();
		
        // if the list is empty
		if(currNode == null){
			this.firstNode = node;
			return;
		}
	
		Node prevNode = currNode.getPrev();
		
		while(currNode != null){
            
            boolean condition;
            // if the order is alphabetical
            if(order == 0){
                condition = (currNode.getString().compareToIgnoreCase(node.getString())) > 0;
            }
            // if the order is reverse
            else{
                condition = (currNode.getString().compareToIgnoreCase(node.getString())) < 0;
            }
			
			if(condition){
				Node temp = currNode.getPrev();

                // if we are adding at the beginning
                if(temp == null){
                    currNode.setPrev(node);
                    node.setNext(currNode);
                    this.firstNode = node;
                    return;
                }
                
                // addinf in the middle
				else{
                    currNode.setPrev(node);
				    temp.setNext(node);
				    node.setNext(currNode);
				    node.setPrev(temp);
				    return;
                }
			}
            // iterate
			prevNode = currNode;
			currNode = currNode.getNext();
		}
        // adding at the end
        prevNode.setNext(node);
        node.setPrev(prevNode);
    }


    @Override
    public Node getFirst(){
		return this.firstNode;
	}


    @Override
	public Node getLast(){
        Node currNode = this.getFirst();
		// if the list is empty
		if(currNode==null){
			return null;
		}
		else{
			while(currNode.getNext() != null){
				currNode = currNode.getNext();
			}
            return currNode;
        }
	}


    @Override
	public Node get(int index){
		if(index < 0){return null;}
		if(index >= this.size()){return null;}

		else{
			Node currNode = this.getFirst();
			for(int i=0; i<index; i++){
				currNode = currNode.getNext();
			}
			return currNode;
		}
	}


    @Override
	public boolean isPresent(String string){
		Node currNode = this.getFirst();
		
		// if the list is empty
		if(currNode==null){
			return false;
		}
		else{
			while(currNode.getNext() != null){
				if(currNode.getString().compareToIgnoreCase(string) == 0){
					return true;
				}
				currNode = currNode.getNext();
			}
			if(currNode.getString().compareToIgnoreCase(string) == 0){
				return true;
			}
			return false;
		}
	}

	
	@Override
	public boolean removeFirst(){
		if(this.size() == 0){return false;}

		else if(this.size() == 1){
			this.firstNode = null;
			return true;
		}
		else{
			this.firstNode.getNext().setPrev(null);
			this.firstNode = this.firstNode.getNext();
			return true;
		}
	}

    
    @Override
	public boolean removeLast(){
        // empty list
		if(this.size() == 0){return false;}

        // one element
        else if(this.size()==1){
            this.firstNode = null;
            return true;
        }
        else{
            Node currNode = this.getFirst();
            while(currNode.getNext() != null){
				currNode = currNode.getNext();
			}
            currNode.getPrev().setNext(null);
            return true;
        }
	}


    @Override
	public boolean remove(int index){
        // empty list
		if(this.size() == 0){return false;}
        if(index < 0){return false;}
		if(index >= this.size()){return false;}
        
        else{
            // if we are removing the first element
            if(index == 0){
                this.firstNode = this.firstNode.getNext();
                return true;
            }

			Node currNode = this.getFirst();
			for(int i=0; i<index; i++){
				currNode = currNode.getNext();
			}
            currNode.getPrev().setNext(currNode.getNext());
            // if it is not the last element
            if(currNode.getNext() != null){
                currNode.getNext().setPrev(currNode.getPrev());
            }
            
			return true;
		}
	}


    @Override
	public boolean remove(String string){
        Node currNode = this.getFirst();
		// if the list is empty
		if(this.size()==0){
			return false;
		}
        // first element
        if(currNode.getString().compareToIgnoreCase(string)==0){
            this.remove(0);
            return true;
        }
		else{
            int count = 0;
			while(currNode.getNext() != null){
				if(currNode.getString().compareToIgnoreCase(string)==0){
                    this.remove(count);
                    return true;
                }
				currNode = currNode.getNext();
                count++;
			}
            // last element
            if(currNode.getString().compareToIgnoreCase(string)==0){
                this.remove(count);
                return true;
            }
            // it's not in the list
            return false;
		}
	}


    @Override
	public void orderAscending(){
        // already ordered alphabetically
        if(this.order==0){return;}
        this.switchLinks();
        this.order = 0;
	}


    @Override
	public void orderDescending(){
        // already ordered reverse alphabetically
        if(this.order==1){return;}
        this.switchLinks();
        this.order = 1;
	}


    public void switchLinks(){
        if(this.size() == 0 || this.size() == 1){
            return;
        }
        else{

            Node currNode = this.getFirst();

            while(currNode.getNext() != null){
                Node temp = currNode.getNext();
				currNode.setNext(currNode.getPrev());
                currNode.setPrev(temp);
                currNode = temp;
			}

            // last node
            Node temp = currNode.getNext();
			currNode.setNext(currNode.getPrev());
            currNode.setPrev(temp);
            // set the end of the list as the head
            this.firstNode = currNode;
        }
    }

    
    @Override
	public void print(){        
		Node currNode = this.getFirst();
		// if the list is empty
		if(currNode==null){
			return;
		}
		else{
			// print the head
			System.out.println(currNode.getString());
			// print the rest of the nodes, if any
			while(currNode.getNext() != null){
				System.out.println(currNode.getNext().getString());
				currNode = currNode.getNext();
			}
		}
	}
}