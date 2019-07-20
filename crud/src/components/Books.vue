<template>
  <div id="books">
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Books</h1>
          <hr>
          <br>
          <br>
          <alert :message="message" v-if="showMessage"></alert>
          <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add Book</button>
          <br>
          <br>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Title</th>
                <th scope="col">Author</th>
                <th scope="col">Read</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(book,i) in books" :key="i">
                <td>{{book.title}}</td>
                <td>{{book.author}}</td>
                <td>
                  <span v-if="book.reading>0">Yes</span>
                  <span v-else>No</span>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-warning btn-sm" v-b-modal.book-editModal @click="editBook(book)">Update</button>
                    <button type="button" class="btn btn-danger btn-sm" @click="deleteBook(book.id)">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- addBookModalStart -->
      <b-modal ref="addBookModal" id="book-modal" title="Add a new book" hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
            <b-form-input 
              id="form-title-input"
              type="text"
              v-model="addBookForm.title"
              required
              placeholder="Enter title"
            ></b-form-input>
          </b-form-group>
          <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
            <b-form-input
              id="form-author-input"
              type="text"
              v-model="addBookForm.author"
              required
              placeholder="Enter author"
            ></b-form-input>
          </b-form-group>
          <b-form-group id="form-read-group">
            <b-form-checkbox-group v-model="addBookForm.read" id="form-checks">
              <b-form-checkbox value=true>Read?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>
      <!-- addBookModalEnd -->
      <!-- editBookmodal -->
      <b-modal ref="editBookModal" id="book-editModal" title="Edit book" hide-footer>
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
            <b-form-input
              id="form-title-input"
              type="text"
              v-model="editBookForm.title"
              required
              placeholder="Enter title"
            ></b-form-input>
          </b-form-group>
          <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
            <b-form-input
              id="form-author-input"
              type="text"
              v-model="editBookForm.author"
              required
              placeholder="Enter author"
            ></b-form-input>
          </b-form-group>
          <b-form-group id="form-read-group">
            <b-form-checkbox-group v-model="editBookForm.read" id="form-checks">
              <b-form-checkbox value=true>Read?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-form>
      </b-modal>
      <!-- editBookmodalEnd -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Alert from './Alert'

export default {
  data() {
    return {
      myclass: ['myclass'],
      books: [],
      addBookForm: {
          title: '',
          author: '',
          read: false
      },
      editBookForm: {
          id: '',
          title: '',
          author: '',
          read: false
      },
      message: '',
      showMessage: false
    };
  },
  components:{
    alert: Alert
  },
  methods: {
    getBooks() {
      axios
        .get("/books")
        .then(res => {
          this.books = res.data;
          console.log(res.data);
        })
        .catch(err => {
          console.error(err);
        });
    },
    editBook(book) {
        this.editBookForm.id=book.id
        this.editBookForm.title=book.title
        this.editBookForm.author=book.author
        this.editBookForm.read=book.reading>0?true:false
    },
    addBooks() {
        axios.post('/books', {
            title: this.addBookForm.title,
            author: this.addBookForm.author,
            read: this.addBookForm.read
        }).then(res=>{
            console.log(res.data)
            this.getBooks()
            this.message = 'Book added!';
            this.showMessage = true;
        }).catch(err=>{
            console.log(err)
            this.getBooks()
        })
    },
    
    updateBook(id) {
      axios.put(`/book/${id}`, {
        title: this.editBookForm.title,
        author: this.editBookForm.author,
        read: this.editBookForm.read
      }).then(res=>{
        console.log(res.data)
        this.getBooks()
        this.message = 'Book updated!';
        this.showMessage = true;
      }).catch(err=>{
        console.log(err)
        this.getBooks()
      })
    },
    deleteBook(id) {
      axios.delete(`/book/${id}`).then(res=>{
        console.log(res.data)
        this.getBooks()
        this.message = 'Book deleted!';
        this.showMessage = true;
      }).catch(err=>{
        console.log(err)
        this.getBooks()
      })
    },
    initForm() {
        this.addBookForm.title= ''
        this.addBookForm.author= ''
        this.addBookForm.read= false

        this.editBookForm.id= ''
        this.editBookForm.title= ''
        this.editBookForm.author=''
        this.editBookForm.read=false

    },
    onSubmit(evt) {
        evt.preventDefault();
        this.$refs.addBookModal.hide()
        // let readed=0
        // if(addBookForm.read==1)
        //     readed=1
        this.addBooks()
        this.initForm()
    },
    onReset(evt) {
        evt.preventDefault();
        this.$refs.addBookModal.hide()
        this.initForm()
    },
    onSubmitUpdate(evt) {
        evt.preventDefault();
        this.$refs.editBookModal.hide()
        // let readed=0
        // if(addBookForm.read==1)
        //     readed=1
        this.updateBook(this.editBookForm.id)
        this.initForm()
    },
    onResetUpdate(evt) {
      evt.preventDefault()
      this.$refs.editBookModal.hide()
      this.initForm()
      this.getBooks()
    }
  },
  created() {
    this.getBooks();
    this.showMessage = false;

  }
};
</script>
<style>

.modal-backdrop
{
    opacity:0.5 !important;
}
</style>


