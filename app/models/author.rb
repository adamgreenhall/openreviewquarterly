class Author < ActiveRecord::Base
  attr_accessible :first_name, :last_name, :biography
  validates_presence_of :first_name, :last_name
  has_many :pieces
  def name
    self.first_name+' '+self.last_name
  end
  def url
    '/people/'+URLify.urlify(self.name,'-')
  end
end
