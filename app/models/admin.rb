class Admin < ActiveRecord::Base
  # Include default devise modules. Others available are:
  # :token_authenticatable, :confirmable,
  # :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable, :recoverable, :rememberable,
    :trackable, :validatable, :omniauthable, :omniauth_providers => [:google_oauth2]

  # Setup accessible (or protected) attributes for your model
  attr_accessible :email, :password, :password_confirmation, :provider, :uid, :avatar
  def self.from_omniauth(auth)
    if admin = Admin.find_by_email(auth.info.email)
      admin.provider = auth.provider
      admin.uid = auth.uid
      admin
    # else # new admin
    #   where(auth.slice(:provider, :uid)).first_or_create do |admin|
    #     admin.provider = auth.provider
    #     admin.uid = auth.uid
    #     admin.adminname = auth.info.name
    #     admin.email = auth.info.email
    #     admin.avatar = auth.info.image
    #   end
    end
  end  
end
