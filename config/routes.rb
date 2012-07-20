Orq::Application.routes.draw do
  devise_for :admins

  root :to => 'home#index'
  get "about" => 'home#about'
  get "next" => 'home#next'
  get "people" => 'authors#all'
  get "submit" => 'home#submit'
  get "admin" => 'admins#index'
  
  get 'pieces/:id' => 'pieces#show', :as => :pieces
  get "authors/:id" => 'authors#show', :as => :authors
  get "issues/:id" => 'issues#show', :as => :issues

  put 'pieces/:id' => 'pieces#update', :as => :pieces
  put "authors/:id" => 'authors#update', :as => :authors
  put "issues/:id" => 'issues#update', :as => :issues


  get ':issue_title'=>'issues#show', :as => :issues
  get "people/:author_name" => 'authors#show', :as => :authors
  get ":issue_title/:piece_title" => 'pieces#show', :as => :pieces
  get 'issues/all'
  
  resources :issues
  resources :authors
  resources :pieces
  

  # The priority is based upon order of creation:
  # first created -> highest priority.

  # Sample of regular route:
  #   match 'products/:id' => 'catalog#view'
  # Keep in mind you can assign values other than :controller and :action

  # Sample of named route:
  #   match 'products/:id/purchase' => 'catalog#purchase', :as => :purchase
  # This route can be invoked with purchase_url(:id => product.id)

  # Sample resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Sample resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Sample resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Sample resource route with more complex sub-resources
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', :on => :collection
  #     end
  #   end

  # Sample resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end

  # You can have the root of your site routed with "root"
  # just remember to delete public/index.html.
  # root :to => 'welcome#index'

  # See how all your routes lay out with "rake routes"

  # This is a legacy wild controller route that's not recommended for RESTful applications.
  # Note: This route will make all actions in every controller accessible via GET requests.
  # match ':controller(/:action(/:id))(.:format)'
end
