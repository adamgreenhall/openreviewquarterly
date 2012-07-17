class Issue < ActiveRecord::Base
  attr_accessible :is_published, :number, :season, :title, :description
  has_many :pieces
  has_many :authors, :through => :pieces
end
