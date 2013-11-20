class Author < ActiveRecord::Base
  attr_accessible :first_name, :last_name, :biography, :image_url
  validates_presence_of :first_name, :last_name
  has_many :pieces
  has_many :illustrations
  
  scope :publishers, where(:last_name=>['Greenhall','Ahillen'], :first_name=>['Michael','Amelia','Adam'])

  
  def name
    self.first_name+' '+self.last_name
  end
  def url
    '/people/'+URLify.urlify(self.name,'-')
  end
end
