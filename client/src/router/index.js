import { createRouter, createWebHistory } from 'vue-router';

import AddBook from '../components/AddBook.vue';
import AddMember from '../components/AddMember.vue';
import BookList from '../components/BookList.vue';
import HomeView from '../components/HomeView.vue';
import ImportBooks from '../components/ImportBooks.vue';
import IssueBook from '../components/IssueBook.vue';
import MemberList from '../components/MemberList.vue';
import ReturnBook from '../components/ReturnBook.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/books', component: BookList },
  { path: '/add-book', component: AddBook },
  { path: '/members', component: MemberList },
  { path: '/add-member', component: AddMember },
  { path: '/issue-book', component: IssueBook },
  { path: '/return-book', component: ReturnBook },
  { path: '/import-books', component: ImportBooks },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
