class Author < ActiveRecord::Base
  attr_accessible :first_name, :last_name, :biography
  has_many :pieces
  def name
    self.first_name+' '+self.last_name
  end
end
